import cv2
import numpy as np
import mediapipe as mp
import time
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf.symbol_database")

# Bảng màu
colors = [(60, 60, 255), (100, 255, 100), (255, 100, 100), (0, 200, 255), (255, 100, 255), (0, 255, 255)]
color_names = ["RED", "GREEN", "BLUE", "YELLOW", "MAGENTA", "CYAN"]
colorIndex = 0

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Độ phân giải HD (1280x720)
frame_width = 1280  
frame_height = 720 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

def get_index_finger_tip(hand_landmarks):
    return (int(hand_landmarks.landmark[8].x * frame_width),
            int(hand_landmarks.landmark[8].y * frame_height))

def get_finger_status(hand_landmarks):
    # Kiểm tra trạng thái của ngón trỏ và ngón giữa
    index_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
    middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
    return index_up, middle_up

smooth_x, smooth_y = 0, 0
smoothing_factor = 0.4
prev_point = None
line_thickness = 5
running = True
prev_time = time.time()

# Cài đặt cửa sổ với tên mới
cv2.namedWindow("DrawingInCamera", cv2.WINDOW_NORMAL)
cv2.resizeWindow("DrawingInCamera", frame_width, frame_height)

while running:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    current_mode = "IDLE"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            tip_x, tip_y = get_index_finger_tip(hand_landmarks)
            index_up, middle_up = get_finger_status(hand_landmarks)
            
            # Làm mượt tọa độ
            if prev_point is None:
                smooth_x, smooth_y = tip_x, tip_y
            else:
                smooth_x = smooth_x + smoothing_factor * (tip_x - smooth_x)
                smooth_y = smooth_y + smoothing_factor * (tip_y - smooth_y)
            
            current_point = (int(smooth_x), int(smooth_y))

            if index_up and middle_up:
                # Chế độ di chuột / Nhấc bút (2 ngón)
                current_mode = "HOVER (Move)"
                prev_point = None 
                
                cv2.circle(frame, (tip_x, tip_y), 10, (255, 255, 255), 2)
                cv2.circle(frame, (tip_x, tip_y), 12, (0, 0, 0), 1)

            elif index_up and not middle_up:
                # Chế độ vẽ (1 ngón)
                current_mode = "DRAWING"
                
                if prev_point is not None:
                    # Cho phép vẽ trên toàn bộ không gian màn hình
                    cv2.line(canvas, prev_point, current_point, colors[colorIndex], line_thickness)
                prev_point = current_point
                
                cv2.circle(frame, (tip_x, tip_y), line_thickness, colors[colorIndex], -1)
                cv2.circle(frame, (tip_x, tip_y), line_thickness + 2, (255, 255, 255), 1)
                
            else:
                # Cụp tay
                current_mode = "RESTING"
                prev_point = None

    # Ghép Canvas vào Frame
    canvas_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(canvas_gray, 1, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    
    frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
    canvas_fg = cv2.bitwise_and(canvas, canvas, mask=mask)
    frame = cv2.add(frame_bg, canvas_fg)

    # Hiển thị HUD thông tin gọn gàng ở góc trái
    cv2.putText(frame, f"Mode: {current_mode}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"Color: {color_names[colorIndex]} (Keys: 1-6)", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, colors[colorIndex], 2)
    cv2.putText(frame, f"Size: {line_thickness} (+/-)", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, "Clear: Backspace | Save: 's' | Quit: 'q'", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    # Tính FPS
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    cv2.putText(frame, f"FPS: {int(fps)}", (20, frame_height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("DrawingInCamera", frame)

    # XỬ LÝ PHÍM TẮT
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):
        running = False
    elif key == ord('s'):
        save_canvas = canvas.copy()
        save_canvas[np.where((save_canvas == [0,0,0]).all(axis=2))] = [255, 255, 255]
        cv2.imwrite("DrawingInCamera.png", save_canvas)
        print("Đã lưu hình ảnh: 'DrawingInCamera.png'")
    elif key == ord('+') or key == ord('='):
        line_thickness = min(line_thickness + 2, 30)
    elif key == ord('-'):
        line_thickness = max(line_thickness - 2, 2)
    # Chọn màu bằng phím 1 đến 6
    elif key == ord('1'): colorIndex = 0
    elif key == ord('2'): colorIndex = 1
    elif key == ord('3'): colorIndex = 2
    elif key == ord('4'): colorIndex = 3
    elif key == ord('5'): colorIndex = 4
    elif key == ord('6'): colorIndex = 5
    # Xóa bản vẽ bằng phím Backspace (Mã ASCII thường là 8 hoặc 127)
    elif key == 8 or key == 127:  
        canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

cap.release()
cv2.destroyAllWindows()