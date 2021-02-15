char receivedChar;
boolean newData = false;

const int ledPin = 13;

void setup() {

  Serial.begin(9600);

  pinMode(ledPin, OUTPUT);

}

void loop() {

  recvInfo();
  lightLED();

}

void recvInfo() {

  if (Serial.available() > 0) {

    receivedChar = Serial.read();
    newData = true;

  }

}

void lightLED() {

  while (newData == true) {

    for (int i = 1; i < 4; i++) {
      digitalWrite(ledPin, HIGH);
      delay(100);
      digitalWrite(ledPin, LOW);
      delay(100);
      digitalWrite(ledPin, HIGH);
      delay(100);
      digitalWrite(ledPin, LOW);
      delay(100);
      digitalWrite(ledPin, HIGH);
      delay(500);
      digitalWrite(ledPin, LOW);
    }
    newData = false;

  }

}