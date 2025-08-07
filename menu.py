# menu.py
import sys
import os
import subprocess
import threading
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class DEJEMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller_process = None
        self.auto_start_enabled = False
        self.tray_icon = None
        self.initUI()
        self.create_tray_icon()
        self.check_auto_start_status()
        
        # Sprawdź, czy uruchomiony z argumentem --background
        if "--background" in sys.argv:
            self.hide_to_tray()

    def initUI(self):
        # Ustawienia okna
        self.setWindowTitle('🎛️ DEJE Controller - Menu główne')
        self.setGeometry(100, 100, 850, 700)
        
        # Tapeta
        background_file = "1234.png"
        if os.path.exists(background_file):
            try:
                background_image = QImage(background_file)
                if not background_image.isNull():
                    scaled_image = background_image.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                    palette = QPalette()
                    palette.setBrush(QPalette.Background, QBrush(scaled_image))
                    self.setPalette(palette)
                    print("✅ Tapeta załadowana pomyślnie")
                else:
                    print("❌ Nie można wczytać obrazu tapety - uszkodzony plik")
                    self.setStyleSheet(" QMainWindow { background-color: #2c3e50; } ")
            except Exception as e:
                print(f"❌ Błąd ładowania tapety: {e}")
                self.setStyleSheet(" QMainWindow { background-color: #2c3e50; } ")
        else:
            print("❌ Plik tapety nie istnieje - używam koloru tła")
            self.setStyleSheet(" QMainWindow { background-color: #2c3e50; } ")
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Nagłówek z ikonkami
        header = QLabel('<h1 style="color: white; text-align: center;">🎛️ DEJE Controller v2.0</h1>')
        layout.addWidget(header)
        
        # Status z ikonkami
        self.status_label = QLabel('🔍 Gotowy do uruchomienia')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("QLabel { font-size: 16px; color: #bdc3c7; font-weight: bold; }")
        layout.addWidget(self.status_label)
        
        # Status kontrolera z ikonkami
        self.controller_status = QLabel('⏹️ Kontroler zatrzymany')
        self.controller_status.setAlignment(Qt.AlignCenter)
        self.controller_status.setStyleSheet("QLabel { font-size: 14px; color: #e74c3c; font-weight: bold; }")
        layout.addWidget(self.controller_status)
        
        # Przyciski główne z ikonkami
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(15)
        
        # Styl dla przycisków z ikonkami
        button_style = """
            QPushButton {
                background-color: rgba(52, 152, 219, 0.95);
                color: white;
                border: none;
                padding: 18px;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: rgba(41, 128, 185, 0.95);
            }
            QPushButton:pressed {
                background-color: rgba(33, 97, 140, 0.95);
            }
        """
        
        # Styl dla przycisku kontrolera (zielony/czerwony)
        self.controller_button_style_running = """
            QPushButton {
                background-color: rgba(231, 76, 60, 0.95);
                color: white;
                border: none;
                padding: 18px;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: rgba(192, 57, 43, 0.95);
            }
            QPushButton:pressed {
                background-color: rgba(150, 40, 30, 0.95);
            }
        """
        
        self.controller_button_style_stopped = """
            QPushButton {
                background-color: rgba(46, 204, 113, 0.95);
                color: white;
                border: none;
                padding: 18px;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: rgba(39, 174, 96, 0.95);
            }
            QPushButton:pressed {
                background-color: rgba(30, 130, 70, 0.95);
            }
        """
        
        self.config_btn = QPushButton('🔧 Konfiguracja')
        self.config_btn.setStyleSheet(button_style)
        self.config_btn.clicked.connect(self.open_configurator)
        btn_layout.addWidget(self.config_btn)
        
        # Przycisk kontrolera - zmienia się w zależności od stanu
        self.controller_btn = QPushButton('▶️ Uruchom kontroler')
        self.controller_btn.setStyleSheet(self.controller_button_style_stopped)
        self.controller_btn.clicked.connect(self.toggle_controller)
        btn_layout.addWidget(self.controller_btn)
        
        self.test_btn = QPushButton('🧪 Test połączenia')
        self.test_btn.setStyleSheet(button_style)
        self.test_btn.clicked.connect(self.test_connection)
        btn_layout.addWidget(self.test_btn)
        
        # Przycisk auto-start z ikonkami
        self.auto_start_btn = QPushButton('🔁 Auto-start: ?')
        self.auto_start_btn.setStyleSheet(button_style)
        self.auto_start_btn.clicked.connect(self.toggle_auto_start)
        btn_layout.addWidget(self.auto_start_btn)
        
        # Nowy przycisk do ukrywania do zasobnika
        self.hide_btn = QPushButton('🔽 Ukryj do zasobnika')
        self.hide_btn.setStyleSheet(button_style)
        self.hide_btn.clicked.connect(self.hide_to_tray)
        btn_layout.addWidget(self.hide_btn)
        
        self.exit_btn = QPushButton('❌ Wyjdź')
        self.exit_btn.setStyleSheet(button_style)
        self.exit_btn.clicked.connect(self.close_application)
        btn_layout.addWidget(self.exit_btn)
        
        layout.addLayout(btn_layout)
        
        # Instrukcje z ikonkami
        instructions = QLabel("""
        <b>📋 Instrukcja obsługi:</b><br>
        🎛️ <b>1.</b> Podłącz Arduino z kodem arduino_code.ino<br>
        🔧 <b>2.</b> Użyj 'Konfiguracja' aby przypisać akcje<br>
        ▶️ <b>3.</b> Uruchom 'Kontroler' aby zacząć sterować<br>
        🔁 <b>4.</b> Włącz 'Auto-start' aby uruchamiać przy starcie systemu<br>
        🧪 <b>5.</b> Testuj połączenie jeśli są problemy<br><br>
        
        <b>💡 Wskazówki:</b><br>
        • Kontroler działa w tle nawet po zamknięciu menu<br>
        • Auto-start można włączyć/wyłączyć w każdej chwili<br>
        • Konfiguracja zapisuje się automatycznie<br>
        • Status auto-startu jest zapamiętywany<br>
        • Użyj 'Ukryj do zasobnika' aby schować aplikację<br>
        • Dwuklik na ikonie w zasobniku przywraca okno
        """)
        instructions.setStyleSheet("""
            QLabel { 
                background-color: rgba(0, 0, 0, 150); 
                padding: 20px; 
                border-radius: 15px;
                font-size: 13px;
                color: white;
            }
        """)
        layout.addWidget(instructions)
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_background()
        
    def update_background(self):
        background_file = "1234.png"
        if os.path.exists(background_file):
            try:
                background_image = QImage(background_file)
                if not background_image.isNull():
                    scaled_image = background_image.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                    palette = QPalette()
                    palette.setBrush(QPalette.Background, QBrush(scaled_image))
                    self.setPalette(palette)
            except Exception as e:
                print(f"❌ Błąd aktualizacji tapety: {e}")
                
    def toggle_controller(self):
        if self.controller_process is None:
            self.start_controller()
        else:
            self.stop_controller()
            
    def start_controller(self):
        if not os.path.exists('controller.py'):
            self.show_error_message("❌ Błąd", "Nie znaleziono pliku controller.py")
            return
            
        try:
            # Ustaw katalog roboczy na katalog skryptu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            controller_path = os.path.join(script_dir, 'controller.py')
            if not os.path.exists(controller_path):
                self.show_error_message("❌ Błąd", f"Nie znaleziono pliku:\n{controller_path}")
                return
                
            # Uruchom kontroler BEZ pokazywania okna konsoli
            self.controller_process = subprocess.Popen([
                sys.executable, 
                controller_path
            ], 
            cwd=script_dir,  # Ustaw katalog roboczy
            creationflags=subprocess.CREATE_NO_WINDOW)  # UKRYJ okno konsoli
            
            self.controller_btn.setText('⏹️ Zatrzymaj kontroler')
            self.controller_btn.setStyleSheet(self.controller_button_style_running)
            self.controller_status.setText('▶️ Kontroler uruchomiony')
            self.status_label.setText("✅ Kontroler działa")
            print("✅ Kontroler uruchomiony w tle")
        except Exception as e:
            self.show_error_message("❌ Błąd", f"Nie można uruchomić kontrolera:\n{str(e)}")
            self.controller_process = None
            
    def stop_controller(self):
        if self.controller_process:
            try:
                self.controller_process.terminate()
                self.controller_process.wait(timeout=3)
            except:
                try:
                    self.controller_process.kill()
                except:
                    pass
            self.controller_process = None
            self.controller_btn.setText('▶️ Uruchom kontroler')
            self.controller_btn.setStyleSheet(self.controller_button_style_stopped)
            self.controller_status.setText('⏹️ Kontroler zatrzymany')
            self.status_label.setText("🔍 Gotowy do uruchomienia")
            print("⏹️ Kontroler zatrzymany")
            
    def check_auto_start_status(self):
        """Sprawdza aktualny status auto-startu"""
        try:
            import winreg
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            app_name = "DEJE_Controller"
            
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            try:
                winreg.QueryValueEx(key, app_name)
                self.auto_start_enabled = True
                self.auto_start_btn.setText('🔁 Auto-start: WŁĄCZONY')
                self.status_label.setText("✅ Auto-start włączony")
            except FileNotFoundError:
                self.auto_start_enabled = False
                self.auto_start_btn.setText('🔁 Auto-start: WYŁĄCZONY')
                self.status_label.setText("🔍 Gotowy do uruchomienia")
            winreg.CloseKey(key)
        except Exception as e:
            print(f"❌ Błąd sprawdzania auto-startu: {e}")
            self.auto_start_enabled = False
            self.auto_start_btn.setText('🔁 Auto-start: WYŁĄCZONY')
            
    def toggle_auto_start(self):
        """Przełącza auto-start"""
        if self.auto_start_enabled:
            # Wyłącz auto-start
            self.remove_startup()
        else:
            # Włącz auto-start
            self.setup_startup()
            
        # Odśwież status
        self.check_auto_start_status()
            
    def setup_startup(self):
        """Ustawia automatyczne uruchamianie przy starcie systemu"""
        try:
            import winreg
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            app_name = "DEJE_Controller"
            
            # Pełna ścieżka do aplikacji
            script_dir = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.join(script_dir, 'menu.py')
            # Uruchamiaj z flagą --background, aby od razu ukryć do zasobnika
            app_path = f'"{sys.executable}" "{script_path}" --background'
            
            # Otwórz klucz rejestru i ustaw wartość
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, app_path)
            winreg.CloseKey(key)
            print("✅ Auto-start ustawiony z flagą --background")
            self.show_info_message("✅ Sukces", "Auto-start został włączony!\n\nAplikacja będzie uruchamiać się automatycznie przy starcie systemu i ukrywać się do zasobnika.")
        except Exception as e:
            print(f"❌ Błąd ustawiania auto-startu: {e}")
            self.show_error_message("❌ Błąd", f"Nie można ustawić auto-startu:\n{str(e)}")
            
    def remove_startup(self):
        """Usuwa automatyczne uruchamianie"""
        try:
            import winreg
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            app_name = "DEJE_Controller"
            
            # Spróbuj usunąć wpis
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.DeleteValue(key, app_name)
                winreg.CloseKey(key)
                print("✅ Auto-start usunięty")
                self.show_info_message("✅ Sukces", "Auto-start został wyłączony!")
            except FileNotFoundError:
                print("ℹ️ Auto-start już był usunięty")
        except Exception as e:
            print(f"❌ Błąd usuwania auto-startu: {e}")
            
    def show_error_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2c3e50;
            }
            QMessageBox QLabel {
                color: white;
                font-size: 13px;
                font-weight: normal;
            }
            QMessageBox QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
            }
            QMessageBox QPushButton:hover {
                background-color: #34495e;
            }
        """)
        msg.exec_()
        
    def show_info_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #3498db;
            }
            QMessageBox QLabel {
                color: white;
                font-size: 13px;
                font-weight: normal;
            }
            QMessageBox QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
            }
            QMessageBox QPushButton:hover {
                background-color: #34495e;
            }
        """)
        msg.exec_()
        
    def open_configurator(self):
        if not os.path.exists('configurator.py'):
            self.show_error_message("❌ Błąd", "Nie znaleziono pliku configurator.py\nUpewnij się, że wszystkie pliki są w tym samym folderze!")
            return
            
        try:
            # Uruchom configurator w tym samym katalogu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            subprocess.Popen([sys.executable, 'configurator.py'], cwd=script_dir)
            self.status_label.setText("✅ Otwarto konfigurator")
            self.show_info_message("✅ Sukces", "Konfigurator został uruchomiony w osobnym oknie")
        except Exception as e:
            self.show_error_message("❌ Błąd", f"Nie można uruchomić konfiguratora:\n{str(e)}")
    
    def test_connection(self):
        self.status_label.setText("🔄 Testowanie...")
        self.show_info_message("🧪 Test", "🧪 Funkcja testowa - w przyszłych wersjach\n\nSprawdza:\n• Połączenie z Arduino\n• Dostępność portów\n• Poprawność danych\n• Reakcję na zmiany")
        
    def create_tray_icon(self):
        """Tworzy ikonę w zasobniku systemowym"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("❌ Zasobnik systemowy niedostępny")
            return

        # Utwórz ikonę (użyj domyślnej ikony aplikacji lub prostokąt)
        icon = self.style().standardIcon(QStyle.SP_ComputerIcon) # Lub wczytaj własną ikonę .ico
        
        self.tray_icon = QSystemTrayIcon(icon, self)
        self.tray_icon.setToolTip("DEJE Controller")
        
        # Menu kontekstowe dla zasobnika
        tray_menu = QMenu()
        restore_action = QAction("🔧 Przywróć", self)
        restore_action.triggered.connect(self.showNormal)
        tray_menu.addAction(restore_action)
        
        quit_action = QAction("❌ Wyjdź", self)
        quit_action.triggered.connect(self.close_application)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        
        # Połącz dwuklik z przywracaniem okna
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        
        self.tray_icon.show()
        print("✅ Ikona w zasobniku utworzona")
        
    def on_tray_icon_activated(self, reason):
        """Obsługuje akcje na ikonie zasobnika"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()
            self.raise_()
            self.activateWindow()
            
    def hide_to_tray(self):
        """Ukrywa okno do zasobnika"""
        self.hide()
        if self.tray_icon:
            self.tray_icon.showMessage(
                "🎛️ DEJE Controller",
                "Aplikacja działa w tle. Kliknij ikonę, aby przywrócić.",
                QSystemTrayIcon.Information,
                2000
            )
            
    def showNormal(self):
        """Przywraca okno z zasobnika"""
        super().showNormal()
        self.raise_()
        self.activateWindow()
        
    def close_application(self):
        """Zamyka całą aplikację"""
        reply = QMessageBox.question(
            self, 
            '❓ Potwierdzenie', 
            'Czy na pewno chcesz zamknąć DEJE Controller?\n(Kontroler również zostanie zatrzymany)',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.stop_controller() # Zatrzymaj kontroler przed zamknięciem
            # Usuń ikonę zasobnika
            if self.tray_icon:
                self.tray_icon.hide()
                self.tray_icon = None
            QApplication.quit() # Zamknij aplikację
            
    def closeEvent(self, event):
        """Obsługuje zamknięcie okna"""
        # Zamiast zamykać, ukryj do zasobnika
        event.ignore()
        self.hide_to_tray()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Sprawdź, czy instancja już działa (opcjonalnie)
    # Można dodać mechanizm single instance
    
    window = DEJEMenu()
    window.show()
    
    sys.exit(app.exec_())