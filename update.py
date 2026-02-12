import warnings
# Tắt tất cả các cảnh báo từ thư viện requests/urllib3
warnings.filterwarnings("ignore", category=UserWarning, module='requests')
warnings.filterwarnings("ignore", message=".*urllib3.*")

import os
import requests
import subprocess
import time
import sys

GITHUB_RELEASE_URL = "https://github.com/Khoa-It/Chatapp_CMD/releases/latest/download/ChatApp_CMD.zip"

def main():
    print("--- Updating Chat App ---")
    try:
        app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        zip_path = os.path.join(app_dir, "update.zip")
        bat_path = os.path.join(app_dir, "finish_upd.bat")
        
        # [1/3] Tải bản mới
        print("[1/3] Downloading latest version...")
        response = requests.get(GITHUB_RELEASE_URL, timeout=30)
        response.raise_for_status()
        
        with open(zip_path, 'wb') as f:
            f.write(response.content)

        # [2/3] Chuẩn bị kịch bản "ve sầu thoát xác" bằng file Batch
        print("[2/3] Preparing installation...")
        # File BAT này sẽ đợi updater.exe tắt hẳn rồi mới ghi đè tất cả
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write(f"""@echo off
title Chat App Installer
timeout /t 2 /nobreak > nul
echo ---------------------------------------
echo Installing updates, please wait...
powershell Expand-Archive -Path "{zip_path}" -DestinationPath "{app_dir}" -Force
del "{zip_path}"
echo ---------------------------------------
echo Update Successful!
echo You can now close this window and relaunch the app.
pause
del "%~f0"
""")

        # [3/3] Kích hoạt file BAT và tự đóng bản thân
        print("[3/3] Launching installer. This app will close now...")
        subprocess.Popen([bat_path], shell=True)
        
        # Thoát ngay lập tức để giải phóng file updater.exe cho file BAT ghi đè
        time.sleep(1)
        os._exit(0)
            
    except Exception as e:
        print(f"Error Update: {e}")
        input("Press enter to exit...")

if __name__ == "__main__":
    main()
