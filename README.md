# project_HandTrackBot
# Hand Gesture Controlled Car

Control a car using hand gestures via webcam detection. This project uses Python for hand tracking and Arduino for motor control.

## Features
- **Real-time Hand Tracking**: Utilizes MediaPipe to detect hand landmarks.
- **Gesture Commands**:
  - 👋 All fingers up → Move **Forward** ('F')
  - ☝️ Index finger up → Turn **Right** ('R')
  - ✌️ Index and Middle fingers up → Turn **Left** ('L')
  - 🖐️ Four fingers up (index, middle, ring, pinky) → Move **Backward** ('B')
  - ✊ Fist (all fingers down) → **Stop** ('S')
- **Serial Communication**: Commands sent via Bluetooth/Serial to Arduino.

## Hardware Requirements
- Arduino Uno/Nano
- Motor Driver (e.g., L298N)
- 2x DC Motors
- Bluetooth Module (e.g., HC-05/HC-06)
- Webcam
- Chassis, Wheels, and Battery

## Wiring Guide
Connect components as follows:
| Arduino Pin | Component      | Pin(s)          |
|-------------|----------------|-----------------|
| 3 (RX)      | Bluetooth TX   |                 |
| 4 (TX)      | Bluetooth RX   |                 |
| 7, 8, 9     | Motor 1        | IN1, IN2, EN    |
| 10, 11, 12  | Motor 2        | IN1, IN2, EN    |

## Software Setup
1. **Arduino IDE**:
   - Upload `HandTrackCar.ino` to the Arduino.
   - Ensure the `SoftwareSerial` library is installed.

2. **Python Dependencies**:
   ```bash
   pip install opencv-python mediapipe numpy pyserial
