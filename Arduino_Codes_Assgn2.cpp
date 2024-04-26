#include <Servo.h>

Servo servoMotor;

int targetAngle = 0;
unsigned long lastChangeTime = 0;
int ledPin = 11;
bool isMoving = false;

const int trigPin = 9;
const int echoPin = 10;
const int ldrPin = A1;
const int pirPin = 7; // PIR motion sensor pin

unsigned long lastPulseTime = 0;
const unsigned long pulseInterval = 2000; // 1 minute interval

void setup() {
    servoMotor.attach(3);
    servoMotor.write(0); // Set initial position to 0 degrees
    Serial.begin(9600);
    pinMode(ledPin, OUTPUT);
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    pinMode(ldrPin, INPUT);
    pinMode(pirPin, INPUT); // Initialize the PIR sensor pin as an input
}

bool isMotionDetected() {
    int pirValue = digitalRead(pirPin); // Read the PIR sensor value
    if (pirValue == HIGH) {
        return true; // Motion detected
    } else {
        return false; // No motion detected
    }
}

void dispenseFood() {
    targetAngle = 38; // Set target angle to 30 degrees
    lastChangeTime = millis(); // Save the time when the angle was last changed
    isMoving = true;
    digitalWrite(ledPin, HIGH); // Turn on the LED
}

void loop() {
    if (Serial.available() > 0) {
        char command = Serial.read();
        if (command == '1') {
            dispenseFood();
        }
    }

        // Check for motion detection
    if (isMotionDetected()) {
        dispenseFood();
    }

    unsigned long elapsedTime = millis() - lastChangeTime;
    if (isMoving) {
        if (elapsedTime < 1000) { // Hold the position for 1 second
            servoMotor.write(targetAngle); // Rotate to the target angle
        } else {
            servoMotor.write(0); // Return to 0 degrees
            targetAngle = 0; // Reset the target angle
            isMoving = false;
            digitalWrite(ledPin, LOW); // Turn off the LED
        }
    }



    // Check if it's time to pulse the sensor
    if (millis() - lastPulseTime >= pulseInterval) {
        lastPulseTime = millis();
        // Perform ultrasonic sensor pulse
        long duration;
        int distance;
        digitalWrite(trigPin, LOW);
        delayMicroseconds(2);
        digitalWrite(trigPin, HIGH);
        delayMicroseconds(10);
        digitalWrite(trigPin, LOW);
        duration = pulseIn(echoPin, HIGH);
        distance = duration * 0.034 / 2;

        // Read LDR value
        int ldrValue = analogRead(ldrPin);
        if (ldrValue < 100) {
            Serial.println("dark");
        } else {
            Serial.println("light");
        }

        if (distance <= 8) {
            Serial.println("full");
        } else if (distance >= 10) {
            Serial.println("low");
        }
    }

    delay(1000); // Delay for stability
}