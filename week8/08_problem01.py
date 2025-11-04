# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# 모터 제어 핀 번호 (BCM 모드)
PWMA = 18   # 왼쪽 모터 속도 제어 (PWM)
PWMB = 23   # 오른쪽 모터 속도 제어 (PWM)
AIN1 = 22   # 왼쪽 모터 방향 제어 1
AIN2 = 27   # 왼쪽 모터 방향 제어 2
BIN1 = 25   # 오른쪽 모터 방향 제어 1
BIN2 = 24   # 오른쪽 모터 방향 제어 2

# 스위치 핀 번호
SW1 = 5     # 전진
SW2 = 6     # 우회전
SW3 = 13    # 좌회전
SW4 = 19    # 후진

# 스위치 입력 설정 (풀다운 저항 사용)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 모터 출력 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

# PWM 객체 생성 (주파수 500Hz)
L_Motor = GPIO.PWM(PWMA, 500)
L_Motor.start(0)  # 왼쪽 모터 정지
R_Motor = GPIO.PWM(PWMB, 500)
R_Motor.start(0)  # 오른쪽 모터 정지

# 앞으로 전진
def forward():
    stop()
    time.sleep(0.02)
    print('forward button')
    GPIO.output(AIN1, 0)
    GPIO.output(AIN2, 1)
    GPIO.output(BIN1, 0)
    GPIO.output(BIN2, 1)
    L_Motor.ChangeDutyCycle(50)
    R_Motor.ChangeDutyCycle(50)

# 오른쪽 회전
def right():
    stop()
    time.sleep(0.02)
    print('right button')
    GPIO.output(AIN1, 0)
    GPIO.output(AIN2, 1)
    GPIO.output(BIN1, 0)
    GPIO.output(BIN2, 1)
    L_Motor.ChangeDutyCycle(100)
    R_Motor.ChangeDutyCycle(50)

# 왼쪽 회전
def left():
    stop()
    time.sleep(0.02)
    print('left button')
    GPIO.output(AIN1, 0)
    GPIO.output(AIN2, 1)
    GPIO.output(BIN1, 0)
    GPIO.output(BIN2, 1)
    L_Motor.ChangeDutyCycle(50)
    R_Motor.ChangeDutyCycle(100)

# 후진
def back():
    stop()
    time.sleep(0.02)
    print('back button')
    GPIO.output(AIN1, 1)
    GPIO.output(AIN2, 0)
    GPIO.output(BIN1, 1)
    GPIO.output(BIN2, 0)
    L_Motor.ChangeDutyCycle(50)
    R_Motor.ChangeDutyCycle(50)

# 정지
def stop():
    print('stop button')
    GPIO.output(AIN1, 1)
    GPIO.output(AIN2, 1)
    GPIO.output(BIN1, 1)
    GPIO.output(BIN2, 1)
    L_Motor.ChangeDutyCycle(0)
    R_Motor.ChangeDutyCycle(0)

import threading
import serial
import time

bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

gData = ""

def serial_thread():
    global gData
    while True:
        data = bleSerial.readline()
        gData = data.decode('ascii', errors='ignore').strip()



def main():
    global gData
    try:
        while True:
            if gData.find("go") >= 0: # go 수신 시 forward() 실행
                gData = ""
                forward()
            elif gData.find("back") >= 0: # back 수신 시 back() 실행
                gData = ""
                back()
            elif gData.find("left") >= 0: # left 수신 시 left() 실행
                gData = ""
                left()
            elif gData.find("right") >= 0: # right 수신 시 right() 실행
                gData = ""
                right()
            elif gData.find("stop") >= 0: # stop 수신 시 stop() 실행
                gData = ""
                stop()

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    task1 = threading.Thread(target = serial_thread)
    task1.start()
    main()
    bleSerial.close()

# GPIO 핀 초기화
GPIO.cleanup()