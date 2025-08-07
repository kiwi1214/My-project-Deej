@echo off
REM Ukrywa okno konsoli i uruchamia menu.py

REM Sprawdź, czy plik menu.py istnieje
if not exist "menu.py" (
    echo ❌ Nie znaleziono pliku menu.py
    echo 💡 Upewnij się, że plik znajduje się w tym samym folderze
    timeout /t 3 >nul
    exit /b 1
)

REM Uruchom menu.py w ukrytej konsoli
start "" /min pythonw.exe menu.py

if %errorlevel% equ 0 (
    echo ✅ DEJE Controller uruchomiony w tle
) else (
    echo ❌ Błąd uruchamiania DEJE Controller: %errorlevel%
)

exit /b 0