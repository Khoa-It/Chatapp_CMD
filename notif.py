import sys
from win10toast import ToastNotifier

def main():
    # Lấy nội dung tin nhắn từ tham số truyền vào
    if len(sys.argv) > 1:
        msg = " ".join(sys.argv[1:])
    else:
        msg = "Bạn có tin nhắn mới!"
    
    try:
        toaster = ToastNotifier()
        # Không dùng threaded=True ở đây vì file này chạy độc lập rồi
        toaster.show_toast(
            "Chat App",
            msg,
            duration=3,
            icon_path="" # Bạn có thể thêm file .ico vào đây
        )
    except Exception:
        sys.exit()
    
if __name__ == "__main__":
    main()
