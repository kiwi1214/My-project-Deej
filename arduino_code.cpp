void setup() {
  Serial.begin(9600);
  
  // Inicjalizacja pinów analogowych (A0-A4)
  for (int i = 0; i < 5; i++) {
    pinMode(A0 + i, INPUT);
  }
  
  // Inicjalizacja przycisków (D2-D6)
  for (int i = 2; i < 7; i++) {
    pinMode(i, INPUT_PULLUP);
  }
  
  Serial.println("Arduino DEJE Ready");
}

void loop() {
  String potData = "POT:";
  String btnData = "|BTN:";
  
  // Odczyt suwaków (0-1023)
  for (int i = 0; i < 5; i++) {
    potData += analogRead(A0 + i);
    if (i < 4) potData += ",";
  }
  
  // Odczyt przycisków (0 lub 1)
  for (int i = 0; i < 5; i++) {
    btnData += digitalRead(2 + i) == LOW ? "1" : "0";
    if (i < 4) btnData += ",";
  }
  
  Serial.println(potData + btnData);
  delay(50);  // 20 FPS
}