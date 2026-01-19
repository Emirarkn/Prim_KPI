@echo off
chcp 65001 >nul
echo ╔════════════════════════════════════════════════════════════╗
echo ║   Pharma Sales Incentive System - Kurulum Scripti          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

:: Python kontrolü
echo [1/5] Python kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı! Lütfen Python 3.10+ yükleyin.
    echo    İndirmek için: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python bulundu

:: Sanal ortam oluştur
echo.
echo [2/5] Sanal ortam oluşturuluyor...
if exist "venv" (
    echo    Mevcut venv bulundu, siliniyor...
    rmdir /s /q venv
)
python -m venv venv
if errorlevel 1 (
    echo ❌ Sanal ortam oluşturulamadı!
    pause
    exit /b 1
)
echo ✅ Sanal ortam oluşturuldu

:: Sanal ortamı aktive et
echo.
echo [3/5] Sanal ortam aktive ediliyor...
call venv\Scripts\activate.bat
echo ✅ Sanal ortam aktive edildi

:: Pip güncelle
echo.
echo [4/5] Pip güncelleniyor...
python -m pip install --upgrade pip >nul 2>&1
echo ✅ Pip güncellendi

:: Bağımlılıkları yükle
echo.
echo [5/5] Bağımlılıklar yükleniyor...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Bağımlılıklar yüklenemedi!
    pause
    exit /b 1
)
echo ✅ Bağımlılıklar yüklendi

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   ✅ KURULUM TAMAMLANDI!                                   ║
echo ╠════════════════════════════════════════════════════════════╣
echo ║                                                            ║
echo ║   Uygulamayı başlatmak için:                              ║
echo ║   1. VS Code'da bu klasörü açın                           ║
echo ║   2. F5 tuşuna basın veya                                 ║
echo ║   3. "run.bat" dosyasını çalıştırın                       ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
pause
