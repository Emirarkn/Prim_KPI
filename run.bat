@echo off
chcp 65001 >nul
echo ╔════════════════════════════════════════════════════════════╗
echo ║   Pharma Sales Incentive System                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

:: Sanal ortam kontrolü
if not exist "venv" (
    echo ❌ Sanal ortam bulunamadı!
    echo    Lütfen önce setup.bat dosyasını çalıştırın.
    pause
    exit /b 1
)

:: Aktive et ve çalıştır
echo 🚀 Uygulama başlatılıyor...
echo.
call venv\Scripts\activate.bat
python src/main.py

if errorlevel 1 (
    echo.
    echo ❌ Uygulama hata ile kapandı!
    pause
)
