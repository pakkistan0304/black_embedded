# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# 모터 드라이버 제어용 핀 번호 (BCM 모드)
PWMA = 18   # 왼쪽 모터 속도 제어 (PWM)
PWMB = 23   # 오른쪽 모터 속도 제어 (PWM)
AIN1 = 22   # 왼쪽 모터 방향 제어 1
AIN2 = 27   # 왼쪽 모터 방향 제어 2
BIN1 = 25   # 오른쪽 모터 방향 제어 1
BIN2 = 24   # 오른쪽 모터 방향 제어 2

# GPIO 기본 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 각 핀을 출력으로 설정
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

# PWM 객체 생성 (500Hz)
L_Motor = GPIO.PWM(PWMA, 500)  # 왼쪽 모터 PWM
L_Motor.start(0)               # 초기 듀티비 0 (정지)
R_Motor = GPIO.PWM(PWMB, 500)  # 오른쪽 모터 PWM
R_Motor.start(0)               # 초기 듀티비 0 (정지)

try:
    while True:
        # 정방향 회전: 두 모터 같은 방향으로 설정
        GPIO.output(AIN1, 0)
        GPIO.output(AIN2, 1)
        GPIO.output(BIN1, 0)
        GPIO.output(BIN2, 1)

        # 모터 속도 50%로 구동
        L_Motor.ChangeDutyCycle(50)
        R_Motor.ChangeDutyCycle(50)
        time.sleep(1.0)

        # 모터 정지
        L_Motor.ChangeDutyCycle(0)
        R_Motor.ChangeDutyCycle(0)
        time.sleep(1.0)

except KeyboardInterrupt:
    # Ctrl + C 눌렀을 때 루프 종료
    pass

# 프로그램 종료 시 GPIO 리셋
GPIO.cleanup()
