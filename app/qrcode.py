import cv2
from pyzbar.pyzbar import decode


def scan_qr_code_camera():
    # Mở kết nối đến camera (đặt index = 0 cho camera mặc định)
    cap = cv2.VideoCapture(0)

    try:
        # Kiểm tra xem kết nối đến camera có thành công không
        if not cap.isOpened():
            print("Không thể kết nối đến camera.")
            exit()

        while True:
            ret, frame = cap.read()

            # Quét mã QR từ frame
            decoded_objects = decode(frame)

            for obj in decoded_objects:
                data = obj.data.decode("utf-8")

                # Hiển thị dữ liệu mã QR trên frame
                cv2.putText(frame, f"Mã QR: {data}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                return data

            # Hiển thị frame
            cv2.imshow("Camera QR Scanner", frame)

            # Thoát vòng lặp khi nhấn phím 'x'
            if cv2.waitKey(1) & 0xFF == ord('x'):
                break
    except Exception as e:
        print(e)
    finally:
        # Giải phóng camera và đóng cửa sổ hiển thị
        cap.release()
        cv2.destroyAllWindows()


def generate_qr_code(data, file_name='qrcode.png'):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_name)
