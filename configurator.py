import sys
import json
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class DEJEConfigurator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = self.load_config()
        self.initUI()
        
    def load_config(self):
        if not os.path.exists('config.json'):
            self.create_default_config()
            
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Błąd ładowania konfiguracji: {e}")
            return {
                "potentiometers": {},
                "buttons": {}
            }
    
    def create_default_config(self):
        default_config = {
            "potentiometers": {
                "0": "głośność systemowa",
                "1": "głośność aplikacji:chrome.exe",
                "2": "głośność aplikacji:discord.exe",
                "3": "głośność aktywnej aplikacji",
                "4": "głośność mikrofonu"
            },
            "buttons": {
                "0": "wyciszenie systemowe",
                "1": "wyciszenie aplikacji:chrome.exe",
                "2": "wyciszenie aplikacji:discord.exe",
                "3": "wyciszenie aktywnej aplikacji",
                "4": "wyciszenie mikrofonu",
                "5": "▶️⏸️ odtwórz zatrzymaj",
                "6": "⏭️ następny utwór",
                "7": "⏮️ poprzedni utwór",
                "8": "⏹️ zatrzymaj",
                "9": "🔊 zwiększ głośność"
            }
        }
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
    
    def initUI(self):
        self.setWindowTitle('🔧 Konfigurator DEJE - Konfiguracja zaawansowana')
        self.setGeometry(150, 150, 950, 850)
        self.setStyleSheet("QMainWindow { background-color: #ecf0f1; }")
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Nagłówek z ikonkami
        header = QLabel('<h1 style="color: #2c3e50; text-align: center;">🔧 Konfigurator DEJE v2.0</h1>')
        main_layout.addWidget(header)
        
        # Opis z ikonkami
        description = QLabel("""
        <b>🔧 Konfiguracja zaawansowana:</b><br>
        🎚️ 5 suwaków do kontroli głośności<br>
        🔘 10 przycisków do różnych funkcji<br>
        🎮 Możliwość wyboru konkretnych aplikacji<br>
        🎵 Kontrola multimediów<br>
        🎯 Personalizacja akcji
        """)
        description.setStyleSheet("""
            QLabel { 
                background-color: #3498db; 
                color: white;
                padding: 12px; 
                border-radius: 10px;
                font-size: 12px;
            }
        """)
        main_layout.addWidget(description)
        
        # Styl dla przycisków
        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 18px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """
        
        # Scroll area dla konfiguracji
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)
        
        # Popularne aplikacje
        popular_apps = [
            "chrome.exe", "firefox.exe", "opera.exe", "edge.exe",
            "discord.exe", "teamspeak.exe", "skype.exe",
            "vlc.exe", "spotify.exe", "itunes.exe", "foobar2000.exe",
            "steam.exe", "epicgameslauncher.exe", "uplay.exe",
            "PlantsVsZombies.exe", "Minecraft.exe", "Fortnite.exe",
            "Valorant.exe", "csgo.exe", "League of Legends.exe"
        ]
        
        # Dostępne akcje głośności z ikonkami
        volume_actions = [
            "", 
            "🔊 głośność systemowa", 
            "🎧 głośność aktywnej aplikacji", 
            "🎤 głośność mikrofonu"
        ]
        
        # Dodaj aplikacje do akcji głośności
        for app in popular_apps:
            volume_actions.append(f"🔊 głośność aplikacji:{app}")
        
        # Dostępne akcje wyciszenia z ikonkami
        mute_actions = [
            "", 
            "🔇 wyciszenie systemowe", 
            "🔇 wyciszenie aktywnej aplikacji", 
            "🎤 wyciszenie mikrofonu"
        ]
        
        # Dodaj aplikacje do akcji wyciszenia
        for app in popular_apps:
            mute_actions.append(f"🔇 wyciszenie aplikacji:{app}")
        
        # Dostępne akcje multimedialne z ikonkami
        media_actions = [
            "", 
            "▶️⏸️ odtwórz zatrzymaj",
            "⏭️ następny utwór", 
            "⏮️ poprzedni utwór",
            "⏹️ zatrzymaj",
            "🔊 zwiększ głośność",
            "🔉 zmniejsz głośność",
            "🔇 wycisz system",
            "⏩ przewiń do przodu",
            "⏪ przewiń do tyłu",
            "☀️ zwiększ jasność",
            "🌙 zmniejsz jasność",
            "😴 uśpij komputer",
            "🔌 wyłącz komputer",
            "🔒 zablokuj komputer",
            "📸 zrób zrzut ekranu",
            "📋 kopiuj do schowka",
            "📎 wklej ze schowka"
        ]
        
        # Dostępne akcje aplikacji z ikonkami
        app_specific_actions = [
            "", 
            "🚀 uruchom aplikację:chrome.exe",
            "📝 uruchom aplikację:notepad.exe",
            "🧮 uruchom aplikację:calculator.exe",
            "❌ zamknij aplikację:chrome.exe",
            "🔽 minimalizuj wszystkie okna",
            "🖥️ pokaż pulpit",
            "📁 otwórz eksplorator plików",
            "🛠️ otwórz menedżer zadań",
            "⚙️ otwórz panel sterowania"
        ]
        
        # Dostępne akcje API z ikonkami
        api_actions = [
            "", 
            "🎵 spotify:odtwórz",
            "🎵 spotify:zatrzymaj", 
            "🎵 spotify:następny",
            "🎵 spotify:poprzedni",
            "🎵 spotify:głośniej",
            "🎵 spotify:ciszej",
            "🎮 discord:zmień status",
            "🎮 discord:wyciszenie push-to-talk",
            "📱 twitch:rozpocznij stream",
            "📱 twitch:zakończ stream",
            "📱 twitch:zmień tytuł",
            "🌐 http:żądanie GET",
            "🌐 http:żądanie POST"
        ]
        
        # Połącz wszystkie akcje
        all_actions = volume_actions + mute_actions + media_actions + app_specific_actions + api_actions
        
        # Suwaki - 5 suwaków
        pot_group = QGroupBox("🎚️ Konfiguracja Suwaków (0-4)")
        pot_layout = QVBoxLayout()
        pot_layout.setSpacing(12)
        
        self.pot_combos = []
        for i in range(5):
            row = QHBoxLayout()
            label = QLabel(f'<b>Suwak {i}:</b>')
            label.setFixedWidth(90)
            label.setStyleSheet("QLabel { color: #2c3e50; font-size: 12px; }")
            combo = QComboBox()
            combo.addItems(all_actions)
            combo.setEditable(True)
            combo.setStyleSheet("""
                QComboBox {
                    padding: 8px;
                    border: 2px solid #bdc3c7;
                    border-radius: 8px;
                    background-color: white;
                    font-size: 11px;
                }
                QComboBox QAbstractItemView {
                    border: 2px solid #bdc3c7;
                    selection-background-color: #3498db;
                    font-size: 11px;
                }
                QComboBox:hover {
                    border-color: #3498db;
                }
            """)
            current = self.config["potentiometers"].get(str(i), "")
            combo.setCurrentText(current)
            combo.currentTextChanged.connect(lambda text, idx=i: self.update_pot_config(idx, text))
            
            row.addWidget(label)
            row.addWidget(combo)
            pot_layout.addLayout(row)
            self.pot_combos.append(combo)
        
        pot_group.setLayout(pot_layout)
        scroll_layout.addWidget(pot_group)
        
        # Przyciski - 10 przycisków
        btn_group = QGroupBox("🔘 Konfiguracja Przycisków (0-9)")
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(12)
        
        self.btn_combos = []
        for i in range(10):
            row = QHBoxLayout()
            label = QLabel(f'<b>Przycisk {i}:</b>')
            label.setFixedWidth(90)
            label.setStyleSheet("QLabel { color: #2c3e50; font-size: 12px; }")
            combo = QComboBox()
            combo.addItems(all_actions)
            combo.setEditable(True)
            combo.setStyleSheet("""
                QComboBox {
                    padding: 8px;
                    border: 2px solid #bdc3c7;
                    border-radius: 8px;
                    background-color: white;
                    font-size: 11px;
                }
                QComboBox QAbstractItemView {
                    border: 2px solid #bdc3c7;
                    selection-background-color: #3498db;
                    font-size: 11px;
                }
                QComboBox:hover {
                    border-color: #3498db;
                }
            """)
            current = self.config["buttons"].get(str(i), "")
            combo.setCurrentText(current)
            combo.currentTextChanged.connect(lambda text, idx=i: self.update_btn_config(idx, text))
            
            # Dodaj przycisk pomocniczy do wyboru aplikacji
            app_btn = QPushButton('...')
            app_btn.setFixedWidth(35)
            app_btn.setStyleSheet("""
                QPushButton {
                    background-color: #95a5a6;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #7f8c8d;
                }
            """)
            app_btn.clicked.connect(lambda checked, c=combo: self.select_app(c))
            
            row.addWidget(label)
            row.addWidget(combo)
            row.addWidget(app_btn)
            btn_layout.addLayout(row)
            self.btn_combos.append(combo)
        
        btn_group.setLayout(btn_layout)
        scroll_layout.addWidget(btn_group)
        
        # Sekcja API i integracji
        api_group = QGroupBox("🌐 Integracja z API i zewnętrznymi usługami")
        api_layout = QVBoxLayout()
        
        api_text = QLabel("""
        <b>🎵 Spotify API:</b> Kontrola odtwarzania, playlist, głośności<br>
        <b>🎮 Discord API:</b> Status aktywności, wyciszenie, push-to-talk<br>
        <b>📱 Twitch API:</b> Zarządzanie streamem, tytułem, czatem<br>
        <b>🌐 HTTP API:</b> Własne żądania GET/POST do dowolnych usług<br>
        <b>智能家居:</b> Integracja z urządzeniami smart home<br>
        <b>🤖 Makra:</b> Własne skrypty i sekwencje klawiszy
        """)
        api_text.setStyleSheet("""
            QLabel { 
                background-color: #2ecc71; 
                padding: 12px; 
                border-radius: 8px;
                font-size: 11px;
                color: white;
                font-weight: bold;
            }
        """)
        api_layout.addWidget(api_text)
        api_group.setLayout(api_layout)
        scroll_layout.addWidget(api_group)
        
        # Sekcja pomocy z ikonkami
        help_group = QGroupBox("💡 Pomoc i Przykłady")
        help_layout = QVBoxLayout()
        
        help_text = QLabel("""
        <b>📌 Przykłady konfiguracji:</b><br>
        • <b>🔊 głośność aplikacji:PlantsVsZombies.exe</b> - Głośność tylko tej gry<br>
        • <b>🔇 wyciszenie aplikacji:vlc.exe</b> - Wyciszenie VLC<br>
        • <b>▶️⏸️ odtwórz zatrzymaj</b> - Odtwórz/zatrzymaj multimedia<br>
        • <b>⏭️ następny utwór</b> - Następny utwór<br>
        • <b>🚀 uruchom aplikację:notepad.exe</b> - Uruchom Notatnik<br>
        • <b>🎵 spotify:odtwórz</b> - Odtwórz w Spotify<br><br>
        
        <b>🎮 Specjalne opcje:</b><br>
        • Możesz wpisać dowolną nazwę aplikacji .exe<br>
        • Użyj przycisku [...] aby wybrać z listy<br>
        • Wszystkie akcje są wykonywane natychmiast<br>
        • Ikony ułatwiają identyfikację akcji
        """)
        help_text.setStyleSheet("""
            QLabel { 
                background-color: #f8f9fa; 
                padding: 12px; 
                border-radius: 8px;
                font-size: 11px;
                color: #2c3e50;
            }
        """)
        help_layout.addWidget(help_text)
        help_group.setLayout(help_layout)
        scroll_layout.addWidget(help_group)
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        # Przyciski dolne z ikonkami
        button_layout = QVBoxLayout()
        button_layout.setSpacing(12)
        
        # Górny rząd przycisków
        top_row = QHBoxLayout()
        self.save_btn = QPushButton('💾 Zapisz Konfigurację')
        self.save_btn.setStyleSheet(button_style)
        self.save_btn.clicked.connect(self.save_config)
        top_row.addWidget(self.save_btn)
        
        self.reset_btn = QPushButton('🔄 Resetuj do domyślnych')
        self.reset_btn.setStyleSheet(button_style)
        self.reset_btn.clicked.connect(self.reset_config)
        top_row.addWidget(self.reset_btn)
        
        button_layout.addLayout(top_row)
        
        # Dolny rząd przycisków
        bottom_row = QHBoxLayout()
        
        self.presets_btn = QPushButton('🎯 Szablony')
        self.presets_btn.setStyleSheet(button_style)
        self.presets_btn.clicked.connect(self.show_presets)
        bottom_row.addWidget(self.presets_btn)
        
        self.api_btn = QPushButton('🌐 API i Integracje')
        self.api_btn.setStyleSheet(button_style)
        self.api_btn.clicked.connect(self.show_api_config)
        bottom_row.addWidget(self.api_btn)
        
        self.test_btn = QPushButton('🧪 Testuj akcje')
        self.test_btn.setStyleSheet(button_style)
        self.test_btn.clicked.connect(self.test_actions)
        bottom_row.addWidget(self.test_btn)
        
        button_layout.addLayout(bottom_row)
        
        # Przycisk zamknij
        self.close_btn = QPushButton('❌ Zamknij')
        self.close_btn.setStyleSheet(button_style)
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)
        
        main_layout.addLayout(button_layout)
        
        # Status bar
        self.statusBar().showMessage('🔧 Gotowy do konfiguracji zaawansowanej')
        
    def select_app(self, combo):
        """Otwiera okno wyboru aplikacji"""
        dialog = QDialog(self)
        dialog.setWindowTitle("🎯 Wybierz aplikację")
        dialog.setGeometry(200, 200, 450, 550)
        dialog.setStyleSheet("QDialog { background-color: #ecf0f1; }")
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)
        
        # Lista popularnych aplikacji
        apps = [
            "chrome.exe", "firefox.exe", "opera.exe", "edge.exe",
            "discord.exe", "teamspeak.exe", "skype.exe",
            "vlc.exe", "spotify.exe", "itunes.exe", "foobar2000.exe",
            "steam.exe", "epicgameslauncher.exe", "uplay.exe",
            "PlantsVsZombies.exe", "Minecraft.exe", "Fortnite.exe",
            "Valorant.exe", "csgo.exe", "League of Legends.exe",
            "notepad.exe", "calculator.exe", "paint.exe"
        ]
        
        list_widget = QListWidget()
        list_widget.addItems([f"🎮 {app}" for app in apps])
        list_widget.setStyleSheet("""
            QListWidget {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background-color: white;
                font-size: 12px;
            }
            QListWidget::item:hover {
                background-color: #3498db;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #2980b9;
                color: white;
            }
        """)
        list_widget.doubleClicked.connect(lambda: self.select_app_from_list(list_widget, combo, dialog))
        
        layout.addWidget(QLabel("📋 Wybierz aplikację z listy lub wpisz własną:"))
        layout.addWidget(list_widget)
        
        # Pole do wpisania własnej aplikacji
        custom_input = QLineEdit()
        custom_input.setPlaceholderText("✏️ Wpisz nazwę aplikacji (np. moja_gra.exe)")
        custom_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        layout.addWidget(custom_input)
        
        # Przyciski
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("✅ OK")
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        ok_btn.clicked.connect(lambda: self.set_custom_app(custom_input.text(), combo, dialog))
        cancel_btn = QPushButton("❌ Anuluj")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        cancel_btn.clicked.connect(dialog.close)
        
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        dialog.exec_()
        
    def select_app_from_list(self, list_widget, combo, dialog):
        """Wybiera aplikację z listy"""
        selected = list_widget.currentItem()
        if selected:
            app_name = selected.text().replace("🎮 ", "")
            current_text = combo.currentText()
            
            # Sprawdź typ akcji
            if "głośność aplikacji:" in current_text:
                new_text = f"🔊 głośność aplikacji:{app_name}"
            elif "wyciszenie aplikacji:" in current_text:
                new_text = f"🔇 wyciszenie aplikacji:{app_name}"
            elif "uruchom aplikację:" in current_text:
                new_text = f"🚀 uruchom aplikację:{app_name}"
            elif "zamknij aplikację:" in current_text:
                new_text = f"❌ zamknij aplikację:{app_name}"
            else:
                # Domyślnie ustaw jako głośność
                new_text = f"🔊 głośność aplikacji:{app_name}"
                
            combo.setCurrentText(new_text)
            dialog.close()
            
    def set_custom_app(self, app_name, combo, dialog):
        """Ustawia własną aplikację"""
        if app_name:
            current_text = combo.currentText()
            
            # Sprawdź typ akcji
            if "głośność aplikacji:" in current_text:
                new_text = f"🔊 głośność aplikacji:{app_name}"
            elif "wyciszenie aplikacji:" in current_text:
                new_text = f"🔇 wyciszenie aplikacji:{app_name}"
            elif "uruchom aplikację:" in current_text:
                new_text = f"🚀 uruchom aplikację:{app_name}"
            elif "zamknij aplikację:" in current_text:
                new_text = f"❌ zamknij aplikację:{app_name}"
            else:
                # Domyślnie ustaw jako głośność
                new_text = f"🔊 głośność aplikacji:{app_name}"
                
            combo.setCurrentText(new_text)
        dialog.close()
        
    def update_pot_config(self, index, value):
        self.config["potentiometers"][str(index)] = value
        self.statusBar().showMessage(f'✅ Zaktualizowano suwak {index}')
        
    def update_btn_config(self, index, value):
        self.config["buttons"][str(index)] = value
        self.statusBar().showMessage(f'✅ Zaktualizowano przycisk {index}')
        
    def save_config(self):
        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, '✅ Sukces', 'Konfiguracja została zapisana!')
            self.statusBar().showMessage('💾 Konfiguracja zapisana pomyślnie')
        except Exception as e:
            QMessageBox.critical(self, '❌ Błąd', f'Nie udało się zapisać konfiguracji:\n{str(e)}')
            
    def reset_config(self):
        reply = QMessageBox.question(self, '❓ Potwierdzenie', 
                                   'Czy na pewno chcesz zresetować konfigurację do wartości domyślnych?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.create_default_config()
            self.config = self.load_config()
            self.update_ui_from_config()
            self.statusBar().showMessage('🔄 Konfiguracja zresetowana do domyślnych')
            
    def update_ui_from_config(self):
        for i, combo in enumerate(self.pot_combos):
            current = self.config["potentiometers"].get(str(i), "")
            combo.setCurrentText(current)
            
        for i, combo in enumerate(self.btn_combos):
            current = self.config["buttons"].get(str(i), "")
            combo.setCurrentText(current)
            
    def show_presets(self):
        """Pokazuje szablony konfiguracji"""
        presets = {
            "🎮 Gamer Setup": {
                "potentiometers": {
                    "0": "🔊 głośność systemowa",
                    "1": "🔊 głośność aplikacji:discord.exe",
                    "2": "🔊 głośność aplikacji:steam.exe",
                    "3": "🎧 głośność aktywnej aplikacji",
                    "4": "🎤 głośność mikrofonu"
                },
                "buttons": {
                    "0": "🔇 wyciszenie systemowe",
                    "1": "🔇 wyciszenie aplikacji:discord.exe",
                    "2": "▶️⏸️ odtwórz zatrzymaj",
                    "3": "⏭️ następny utwór",
                    "4": "⏮️ poprzedni utwór",
                    "5": "🚀 uruchom aplikację:steam.exe",
                    "6": "🔽 minimalizuj wszystkie okna",
                    "7": "📸 zrób zrzut ekranu",
                    "8": "😴 uśpij komputer",
                    "9": "🎤 wyciszenie mikrofonu"
                }
            },
            "🎵 Media Center": {
                "potentiometers": {
                    "0": "🔊 głośność systemowa",
                    "1": "🔊 głośność aplikacji:vlc.exe",
                    "2": "🔊 głośność aplikacji:spotify.exe",
                    "3": "🎧 głośność aktywnej aplikacji",
                    "4": "🎤 głośność mikrofonu"
                },
                "buttons": {
                    "0": "🔇 wyciszenie systemowe",
                    "1": "▶️⏸️ odtwórz zatrzymaj",
                    "2": "⏭️ następny utwór",
                    "3": "⏮️ poprzedni utwór",
                    "4": "⏹️ zatrzymaj",
                    "5": "🔊 zwiększ głośność",
                    "6": "🔉 zmniejsz głośność",
                    "7": "⏩ przewiń do przodu",
                    "8": "⏪ przewiń do tyłu",
                    "9": "🎤 wyciszenie mikrofonu"
                }
            },
            "📱 Streaming Setup": {
                "potentiometers": {
                    "0": "🔊 głośność systemowa",
                    "1": "🔊 głośność aplikacji:obs64.exe",
                    "2": "🔊 głośność aplikacji:discord.exe",
                    "3": "🎧 głośność aktywnej aplikacji",
                    "4": "🎤 głośność mikrofonu"
                },
                "buttons": {
                    "0": "🔇 wyciszenie systemowe",
                    "1": "🔇 wyciszenie aplikacji:obs64.exe",
                    "2": "🔇 wyciszenie aplikacji:discord.exe",
                    "3": "▶️⏸️ odtwórz zatrzymaj",
                    "4": "📸 zrób zrzut ekranu",
                    "5": "🚀 uruchom aplikację:obs64.exe",
                    "6": "🖥️ pokaż pulpit",
                    "7": "🛠️ otwórz menedżer zadań",
                    "8": "🔒 zablokuj komputer",
                    "9": "🎤 wyciszenie mikrofonu"
                }
            }
        }
        
        dialog = QDialog(self)
        dialog.setWindowTitle("🎯 Szablony konfiguracji")
        dialog.setGeometry(200, 200, 550, 450)
        dialog.setStyleSheet("QDialog { background-color: #ecf0f1; }")
        
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel("<h3>🎯 Wybierz szablon konfiguracji:</h3>"))
        
        for preset_name, preset_config in presets.items():
            btn = QPushButton(preset_name)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #9b59b6;
                    color: white;
                    border: none;
                    padding: 15px;
                    border-radius: 10px;
                    font-weight: bold;
                    font-size: 12px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background-color: #8e44ad;
                }
            """)
            btn.clicked.connect(lambda checked, p=preset_config: self.apply_preset(p, dialog))
            layout.addWidget(btn)
        
        close_btn = QPushButton("❌ Zamknij")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec_()
        
    def apply_preset(self, preset_config, dialog):
        """Aplikuje wybrany szablon"""
        self.config = preset_config
        self.update_ui_from_config()
        self.statusBar().showMessage('🎯 Zastosowano szablon konfiguracji')
        dialog.close()
        
    def show_api_config(self):
        """Pokazuje konfigurację API"""
        dialog = QDialog(self)
        dialog.setWindowTitle("🌐 Konfiguracja API i integracji")
        dialog.setGeometry(200, 200, 600, 500)
        dialog.setStyleSheet("QDialog { background-color: #ecf0f1; }")
        
        layout = QVBoxLayout(dialog)
        
        api_info = QLabel("""
        <h3>🌐 Integracja z zewnętrznymi API</h3>
        
        <b>🎵 Spotify API:</b><br>
        • Kontrola odtwarzania (odtwórz, pauza, następny)<br>
        • Zarządzanie playlistami<br>
        • Kontrola głośności<br>
        • Informacje o aktualnie odtwarzanym utworze<br><br>
        
        <b>🎮 Discord API:</b><br>
        • Status aktywności (Rich Presence)<br>
        • Wyciszenie push-to-talk<br>
        • Zarządzanie kanałami głosowymi<br><br>
        
        <b>📱 Twitch API:</b><br>
        • Zarządzanie streamem<br>
        • Kontrola czatu<br>
        • Informacje o widzach<br><br>
        
        <b>智能家居 Smart Home:</b><br>
        • Integracja z Philips Hue<br>
        • Kontrola urządzeń Xiaomi<br>
        • Sterowanie Alexa/Google Home<br><br>
        
        <b>🤖 Makra i skrypty:</b><br>
        • Własne skrypty PowerShell<br>
        • Sekwencje klawiszy<br>
        • Automatyzacja zadań<br>
        """)
        api_info.setStyleSheet("""
            QLabel { 
                background-color: white; 
                padding: 15px; 
                border-radius: 10px;
                font-size: 11px;
                color: #2c3e50;
            }
        """)
        layout.addWidget(api_info)
        
        close_btn = QPushButton("✅ Zamknij")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec_()
        
    def test_actions(self):
        """Testuje akcje"""
        QMessageBox.information(self, '🧪 Testowanie', 
                              '🧪 Funkcja testowania akcji:\n\n'
                              '• Sprawdza poprawność konfiguracji\n'
                              '• Testuje połączenie z aplikacjami\n'
                              '• Weryfikuje dostępność akcji\n'
                              '• Wyświetla logi działania\n\n'
                              '✨ Funkcja dostępna w wersji PRO!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DEJEConfigurator()
    window.show()
    sys.exit(app.exec_())