Đồng ý, mình đã rà soát và đổi lại toàn bộ tên ứng dụng từ "AirSketch" thành **DrawingInCamera** trong file `README.md` theo đúng ý bạn. (Lưu ý: Mình giữ nguyên link ảnh gốc ở phần Tổng quan để ảnh không bị lỗi hiển thị nhé).

Bạn copy lại toàn bộ nội dung dưới đây để dán vào file `README.md`:

---

# DrawingInCamera: Ứng dụng Vẽ bằng Cử chỉ Tay Thời gian thực 🎨✋

## 📖 Tổng quan

DrawingInCamera là một ứng dụng thị giác máy tính tiên tiến cho phép người dùng vẽ trong không trung bằng các cử chỉ tay. Ứng dụng sử dụng công nghệ theo dõi bàn tay và nhận diện cử chỉ theo thời gian thực để tạo ra một không gian vẽ ảo. Dự án này là minh chứng cho việc kết hợp các kỹ thuật thị giác máy tính (computer vision), thuật toán nhận diện cử chỉ và xử lý video thời gian thực.

## 🛠️ Công nghệ sử dụng

* **Python 3.7+**: Ngôn ngữ lập trình lõi 🐍
* **OpenCV 4.5+**: Thư viện thị giác máy tính dùng để xử lý hình ảnh và hiển thị nét vẽ 📷
* **MediaPipe 0.8.9+**: Framework học máy (machine learning) của Google dùng để theo dõi bàn tay ✋
* **NumPy 1.19+**: Thư viện toán học giúp xử lý mảng (array) với tốc độ cao 📊

## 🌟 Tính năng chính

1. **Theo dõi Bàn tay Thời gian thực**: Sử dụng mô hình nhận diện của MediaPipe để theo dõi 21 điểm (landmarks) trên bàn tay ở định dạng 3D với tốc độ 30+ FPS.
2. **Nhận diện Cử chỉ**: Tích hợp thuật toán tự xây dựng để nhận biết khi nào ngón trỏ giơ lên (bắt đầu vẽ) và khi nào cụp xuống (ngừng vẽ).
3. **Chọn Màu Động**: Cung cấp phím tắt để thay đổi màu sắc nhanh chóng khi đang vẽ mà không cần chạm vào màn hình.
4. **Làm mượt Nét vẽ (Adaptive Smoothing)**: Sử dụng thuật toán làm mượt nội suy (EMA) để giảm độ rung, giúp nét vẽ liền mạch và mượt mà hơn.
5. **Tối ưu Hiệu suất**: Hỗ trợ mở rộng toàn màn hình và tối ưu thuật toán vẽ để hạn chế tối đa độ trễ (latency).
6. **Hiển thị Đa lớp (Multi-layer Rendering)**: Kết hợp luồng video đầu vào với không gian vẽ thông qua kỹ thuật Masking/Alpha blending để tạo ra trải nghiệm liền mạch.

---

## 🚀 Hướng dẫn Cài đặt Thư viện và Chạy file

Để chạy được dự án này, máy tính của bạn cần cài đặt Python và một số thư viện hỗ trợ. Hãy làm theo các bước sau:

### Bước 1: Yêu cầu hệ thống

* Đảm bảo máy tính của bạn đã cài đặt **Python 3.7** trở lên. (Có thể tải tại [python.org](https://www.python.org/)).

### Bước 2: Tải các thư viện cần thiết

Mở **Terminal** (trên macOS/Linux) hoặc **Command Prompt / PowerShell** (trên Windows) và chạy câu lệnh sau để tải toàn bộ thư viện:

```bash
pip install opencv-python mediapipe numpy

```

*(Lưu ý: Chờ một chút để quá trình tải và cài đặt hoàn tất. Nếu bị lỗi, hãy thử dùng `pip3 install...` thay vì `pip`)*

### Bước 3: Tải mã nguồn

Clone kho lưu trữ này về máy hoặc tải file code trực tiếp:

```bash
git clone https://github.com/yourusername/DrawingInCamera.git
cd DrawingInCamera

```

### Bước 4: Chạy file main

Sau khi đã cài đặt đủ thư viện và truy cập vào thư mục chứa code, bạn hãy chạy file Python chính bằng lệnh:

```bash
python DrawingInCamera.py

```

---

## 📋 Hướng dẫn Sử dụng (Khi camera đã bật)

* ✍️ **Để vẽ:** Chỉ giơ duy nhất ngón trỏ lên để vẽ vào không trung.
* 🖱️ **Để di chuyển/nhấc bút:** Giơ cả ngón trỏ và ngón giữa lên.
* 🎨 **Đổi màu:** Bấm các phím số từ `1` đến `6` trên bàn phím.
* 🧹 **Xóa bảng:** Nhấn phím `Backspace` hoặc `Delete`.
* 💾 **Lưu ảnh:** Nhấn phím `s` trên bàn phím (ảnh sẽ được lưu với tên `DrawingInCamera.png`).
* ➕/➖ **Chỉnh nét vẽ:** Nhấn phím `+` hoặc `-` để tăng/giảm độ dày nét bút.
* ❌ **Thoát:** Nhấn phím `q` để tắt ứng dụng.

---

## 🏗️ Kiến trúc Hệ thống

Ứng dụng được thiết kế theo cấu trúc module:

1. **Module Đầu vào**: Chụp và tiền xử lý các khung hình từ webcam.
2. **Module Nhận diện**: Sử dụng MediaPipe để phát hiện và theo dõi các điểm trên tay.
3. **Module Cử chỉ**: Phân tích vị trí các điểm để nhận biết ý định vẽ của người dùng.
4. **Module Vẽ**: Quản lý trạng thái bảng vẽ và tạo nét vẽ dựa trên cử chỉ tay.
5. **Module Giao diện (UI)**: Xử lý hiển thị thông số văn bản lên màn hình (HUD).
6. **Module Đầu ra**: Ghép khung hình gốc, giao diện văn bản và nét vẽ để xuất ra màn hình.

## 🔍 Thuật toán Chính

### Nhận diện điểm trên bàn tay

Sử dụng mô hình phát hiện lòng bàn tay của MediaPipe, kết hợp mô hình điểm mốc (landmark) để trích xuất 21 điểm 3D.

### Phát hiện trạng thái ngón tay

```python
def get_finger_status(hand_landmarks):
    index_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
    middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
    return index_up, middle_up

```

Hàm này so sánh tọa độ để biết ngón trỏ và ngón giữa có đang được giơ lên hay không, từ đó kích hoạt chế độ "Vẽ" hoặc chế độ "Nhấc bút".

### Thuật toán Làm mượt (EMA Smoothing)

```python
smooth_x = smooth_x + smoothing_factor * (tip_x - smooth_x)
smooth_y = smooth_y + smoothing_factor * (tip_y - smooth_y)

```

Tính toán nội suy liên tục giữa điểm nhận diện hiện tại và điểm trước đó để loại bỏ hiện tượng gãy khúc, giúp nét vẽ mềm mại tự nhiên.