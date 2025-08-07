import serial
import serial.tools.list_ports
import json
import time
import os
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import psutil
import win32gui
import win32process

# DOKŁADNE MAPPINGOWANIE CO 1%
THRESHOLD = 0.01

class AudioController:
    def __init__(self):
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
            print("✅ Audio controller zainicjalizowany")
        except Exception as e:
            print(f"❌ Błąd inicjalizacji audio: {e}")
            self.volume = None

    def set_volume(self, process_name, level):
        try:
            sessions = AudioUtilities.GetAllSessions()
            target = process_name.lower()
            for session in sessions:
                proc = session.Process
                if proc and proc.name().lower() == target:
                    session.SimpleAudioVolume.SetMasterVolume(level, None)
                    return True
            return False
        except Exception as e:
            print(f"❌ Błąd ustawiania głośności {process_name}: {e}")
            return False

    def toggle_mute(self, process_name):
        try:
            sessions = AudioUtilities.GetAllSessions()
            target = process_name.lower()
            for session in sessions:
                proc = session.Process
                if proc and proc.name().lower() == target:
                    vol = session.SimpleAudioVolume
                    vol.SetMute(not vol.GetMute(), None)
                    return True
            return False
        except Exception as e:
            print(f"❌ Błąd mute {process_name}: {e}")
            return False

    def set_master(self, level):
        try:
            if self.volume:
                self.volume.SetMasterVolumeLevelScalar(level, None)
                return True
            return False
        except Exception as e:
            print(f"❌ Błąd głośności systemowej: {e}")
            return False

    def toggle_master_mute(self):
        try:
            if self.volume:
                is_muted = self.volume.GetMute()
                self.volume.SetMute(not is_muted, None)
                state = "WŁĄCZONY" if not is_muted else "WYŁĄCZONY"
                print(f"🔇 Mute systemowy: {state}")
                return True
            return False
        except Exception as e:
            print(f"❌ Błąd mute systemowego: {e}")
            return False

    def set_microphone_volume(self, level):
        try:
            import comtypes.client
            from pycaw.pycaw import IMMDeviceEnumerator
            comtypes.CoInitialize()
            enumerator = comtypes.client.CreateObject(
                "{BCDE0395-E52F-467C-8E3D-C4579291692E}",
                interface=IMMDeviceEnumerator
            )
            mic_device = enumerator.GetDefaultAudioEndpoint(1, 1)
            mic_interface = mic_device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            mic_volume = cast(mic_interface, POINTER(IAudioEndpointVolume))
            mic_volume.SetMasterVolumeLevelScalar(level, None)
            return True
        except Exception as e:
            print(f"❌ Błąd głośności mikrofonu: {e}")
            return False

    def toggle_microphone_mute(self):
        try:
            import comtypes.client
            from pycaw.pycaw import IMMDeviceEnumerator
            comtypes.CoInitialize()
            enumerator = comtypes.client.CreateObject(
                "{BCDE0395-E52F-467C-8E3D-C4579291692E}",
                interface=IMMDeviceEnumerator
            )
            mic_device = enumerator.GetDefaultAudioEndpoint(1, 1)
            mic_interface = mic_device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            mic_volume = cast(mic_interface, POINTER(IAudioEndpointVolume))
            is_muted = mic_volume.GetMute()
            mic_volume.SetMute(not is_muted, None)
            state = "WŁĄCZONY" if not is_muted else "WYŁĄCZONY"
            print(f"🎤 Mute mikrofonu: {state}")
            return True
        except Exception as e:
            print(f"❌ Błąd mute mikrofonu: {e}")
            return False

    def set_foreground_app_volume(self, level):
        try:
            hwnd = win32gui.GetForegroundWindow()
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]
            process_name = psutil.Process(pid).name().lower()
            return self.set_volume(process_name, level)
        except Exception as e:
            print(f"❌ Błąd głośności aktywnej aplikacji: {e}")
            return False

    def toggle_foreground_app_mute(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]
            process_name = psutil.Process(pid).name().lower()
            return self.toggle_mute(process_name)
        except Exception as e:
            print(f"❌ Błąd mute aktywnej aplikacji: {e}")
            return False

    def execute_action(self, action, value=None):
        if not action:
            return False
            
        try:
            # Obsługa akcji z ikonkami (nowy format)
            if action == "🔊 głośność systemowa":
                return self.set_master(value)
            elif action.startswith("🔊 głośność aplikacji:"):
                app = action.split(":", 1)[1]
                return self.set_volume(app, value)
            elif action == "🎧 głośność aktywnej aplikacji":
                return self.set_foreground_app_volume(value)
            elif action == "🎤 głośność mikrofonu":
                return self.set_microphone_volume(value)
            elif action == "🔇 wyciszenie systemowe":
                return self.toggle_master_mute()
            elif action.startswith("🔇 wyciszenie aplikacji:"):
                app = action.split(":", 1)[1]
                return self.toggle_mute(app)
            elif action == "🔇 wyciszenie aktywnej aplikacji":
                return self.toggle_foreground_app_mute()
            elif action == "🎤 wyciszenie mikrofonu":
                return self.toggle_microphone_mute()
            
            # Obsługa akcji bez ikonek (stary format - dla kompatybilności wstecznej)
            elif action == "głośność systemowa":
                return self.set_master(value)
            elif action.startswith("głośność aplikacji:"):
                app = action.split(":", 1)[1]
                return self.set_volume(app, value)
            elif action == "głośność aktywnej aplikacji":
                return self.set_foreground_app_volume(value)
            elif action == "głośność mikrofonu":
                return self.set_microphone_volume(value)
            elif action == "wyciszenie systemowe":
                return self.toggle_master_mute()
            elif action.startswith("wyciszenie aplikacji:"):
                app = action.split(":", 1)[1]
                return self.toggle_mute(app)
            elif action == "wyciszenie aktywnej aplikacji":
                return self.toggle_foreground_app_mute()
            elif action == "wyciszenie mikrofonu":
                return self.toggle_microphone_mute()
                
            else:
                print(f"❓ Nieznana akcja: {action}")
                return False
        except Exception as e:
            print(f"❌ Błąd wykonania akcji {action}: {e}")
            return False

def precise_mapping_custom_center(raw_value):
    """
    DOKŁADNE MAPPINGOWANIE Z ŚRODKIEM W 134
    Wartość 134 = dokładnie 50% głośności
    """
    if raw_value <= 134:
        if 134 == 0:
            return 0.0
        normalized = (raw_value - 0) / (134 - 0) * 0.5
    else:
        if 1023 - 134 == 0:
            return 1.0
        normalized = 0.5 + (raw_value - 134) / (1023 - 134) * 0.5
    
    if normalized >= 0.995:
        return 1.0
    elif normalized <= 0.005:
        return 0.0
    
    return normalized

def round_to_percent(value):
    """Zaokrągla wartość do pełnych procentów"""
    return round(value * 100) / 100.0

def find_arduino():
    """Znajduje i łączy się z Arduino"""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "CH340" in port.description or "Arduino" in port.description or "USB" in port.description:
            try:
                ser = serial.Serial(port.device, 9600, timeout=0.1)
                print(f"✅ Arduino połączony: {port.device}")
                return ser
            except Exception as e:
                print(f"❌ Błąd połączenia z {port.device}: {e}")
                continue
    return None

def parse_data(line):
    """Parsuje dane z Arduino"""
    try:
        if "POT:" in line and "|BTN:" in line:
            pot_part, btn_part = line.split("|BTN:")
            pots = [int(x) for x in pot_part[4:].split(",")]
            btns = [int(x) for x in btn_part.split(",")]
            return pots[:5], btns[:10]  # Zmienione z [:5] na [:10]
    except Exception as e:
        print(f"❌ Błąd parsowania: {e}")
    return None, None

def load_config():
    """Ładuje konfigurację"""
    try:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Błąd ładowania konfiguracji: {e}")
        return {
            "potentiometers": {
                "0": "🔊 głośność systemowa",
                "1": "🔊 głośność aplikacji:chrome.exe",
                "2": "🔊 głośność aplikacji:discord.exe",
                "3": "🎧 głośność aktywnej aplikacji",
                "4": "🎤 głośność mikrofonu"
            },
            "buttons": {
                "0": "🔇 wyciszenie systemowe",
                "1": "🔇 wyciszenie aplikacji:chrome.exe",
                "2": "🔇 wyciszenie aplikacji:discord.exe",
                "3": "🔇 wyciszenie aktywnej aplikacji",
                "4": "🎤 wyciszenie mikrofonu",
                "5": "",
                "6": "",
                "7": "",
                "8": "",
                "9": ""
            }
        }

def main():
    print("🎛️ DEJE Controller - Kontrola głośności")
    print("="*50)
    print("🔍 Szukam Arduino...")
    
    # Inicjalizacja
    audio = AudioController()
    config = load_config()
    ser = find_arduino()
    
    if not ser:
        print("❌ Nie znaleziono Arduino - sprawdź połączenie!")
        print("💡 Upewnij się, że Arduino jest podłączone i ma odpowiedni driver")
        input("Naciśnij Enter aby zakończyć...")
        return
    
    if not audio.volume:
        print("❌ Błąd kontroli audio")
        ser.close()
        input("Naciśnij Enter aby zakończyć...")
        return
    
    print("✅ System gotowy!")
    print("🔧 Obracaj potencjometrami i naciskaj przyciski")
    print("📈 Mapowanie aktywne")
    
    last_values = [134] * 5
    last_displayed = [50] * 5
    btn_states = [0] * 10  # Zmienione z [0] * 5 na [0] * 10
    buffer = b""
    
    try:
        while True:
            if ser.in_waiting:
                buffer += ser.read(ser.in_waiting)
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    try:
                        line_str = line.decode('utf-8', errors='ignore').strip()
                        if line_str.startswith("POT:"):
                            pots, btns = parse_data(line_str)
                            
                            if pots:
                                for i, raw_val in enumerate(pots):
                                    if i < 5:
                                        precise_val = precise_mapping_custom_center(raw_val)
                                        last_precise = precise_mapping_custom_center(last_values[i])
                                        
                                        current_percent = round(precise_val * 100)
                                        last_percent = last_displayed[i]
                                        
                                        if abs(current_percent - last_percent) >= 1:
                                            last_values[i] = raw_val
                                            last_displayed[i] = current_percent
                                            
                                            print(f"🎚️ Suwak {i}: {raw_val:4d} → {current_percent:3d}%")
                                            
                                            action = config["potentiometers"].get(str(i), "")
                                            if action:
                                                audio.execute_action(action, precise_val)
                            
                            if btns:
                                for i, state in enumerate(btns):
                                    if i < 10 and state != btn_states[i]:  # Zmienione z i < 5 na i < 10
                                        btn_states[i] = state
                                        if state == 1:
                                            print(f"🔘 Przycisk {i} NACIŚNIĘTY")
                                            
                                            action = config["buttons"].get(str(i), "")
                                            if action:
                                                audio.execute_action(action)
                                                
                    except Exception as e:
                        print(f"❌ Błąd przetwarzania: {e}")
                        
            time.sleep(0.005)
            
    except KeyboardInterrupt:
        print("\n👋 DEJE Controller zakończony")
    except Exception as e:
        print(f"\n❌ Krytyczny błąd: {e}")
    finally:
        if ser:
            ser.close()
        input("Naciśnij Enter aby zakończyć...")

if __name__ == "__main__":
    main()