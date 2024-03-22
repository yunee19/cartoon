import cv2

def cartoonize_frame(frame):
    # Chuyển ảnh sang ảnh xám
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Áp dụng median blur để giảm nhiễu
    gray = cv2.medianBlur(gray, 5)

    # Phát hiện cạnh bằng cách sử dụng adaptive thresholding
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Chuyển ảnh sang ảnh màu
    color = cv2.bilateralFilter(frame, 9, 300, 300)

    # Kết hợp ảnh màu với mặt nạ cạnh
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon

# Đường dẫn của video đầu vào
input_video_path = 'wonoovideo.mp4'

# Tạo đối tượng VideoCapture để đọc video
video_capture = cv2.VideoCapture(input_video_path)

# Lấy kích thước khung hình từ video
frame_width = int(video_capture.get(3))
frame_height = int(video_capture.get(4))
frame_size = (frame_width, frame_height)

# Tạo đối tượng VideoWriter để ghi video đầu ra
output_video_path = 'output_wonoovideook.mp4'
output_video = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, frame_size)

# Xử lý từng khung hình trong video
while True:
    # Đọc khung hình từ video
    ret, frame = video_capture.read()
    if not ret:
        break

    # Áp dụng hiệu ứng cartoon cho khung hình
    cartoon_frame = cartoonize_frame(frame)

    # Ghi khung hình đã xử lý vào video đầu ra
    output_video.write(cartoon_frame)

    # Hiển thị khung hình đã xử lý
    cv2.imshow('Cartoonized Video', cartoon_frame)

    # Thoát khỏi vòng lặp nếu nhấn 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
video_capture.release()
output_video.release()
cv2.destroyAllWindows()
