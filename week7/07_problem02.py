# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# 스위치 핀 번호
SW1 = 5
SW2 = 6
SW3 = 13
SW4 = 19

# 부저 핀과 음계 주파수(Hz)
BUZZER = 12
Do = 261
Re = 294
Mi = 330
Fa = 349
Sol = 392
Ra = 440
Si = 494
hDo = 523

# GPIO 초기 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# PWM 객체 생성 (BUZZER 핀, 초기 주파수 262Hz)
p = GPIO.PWM(BUZZER, 262)
p.start(50)  # 듀티비 50%로 시작 (소리 출력)

# 테스트용: 도~시~높은 도 까지 차례로 재생
p.ChangeFrequency(Do);  time.sleep(0.5)
p.ChangeFrequency(Re);  time.sleep(0.5)
p.ChangeFrequency(Mi);  time.sleep(0.5)
p.ChangeFrequency(Fa);  time.sleep(0.5)
p.ChangeFrequency(Sol); time.sleep(0.5)
p.ChangeFrequency(Ra);  time.sleep(0.5)
p.ChangeFrequency(Si);  time.sleep(0.5)
p.ChangeFrequency(hDo); time.sleep(0.5)
p.stop()  # 부저 정지

# 각각의 스위치가 눌리면 재생할 노래 함수들 -----------------------------

def song1():  # SW1 눌렀을 때 재생
    p.start(50)
    p.ChangeFrequency(Do);  time.sleep(0.5)
    p.ChangeFrequency(Mi);  time.sleep(0.5)
    p.ChangeFrequency(Sol); time.sleep(0.5)
    p.ChangeFrequency(Do);  time.sleep(0.5)
    p.ChangeFrequency(Mi);  time.sleep(0.5)
    p.ChangeFrequency(Sol); time.sleep(0.5)
    p.ChangeFrequency(Ra);  time.sleep(0.5)
    p.ChangeFrequency(Ra);  time.sleep(0.5)
    p.ChangeFrequency(Ra);  time.sleep(0.5)
    p.ChangeFrequency(Sol); time.sleep(0.5)
    p.stop()

def song2():  # SW2 눌렀을 때 재생
    p.start(50)
    p.ChangeFrequency(Mi); time.sleep(0.5)
    p.ChangeFrequency(Re); time.sleep(0.5)
    p.ChangeFrequency(Do); time.sleep(0.5)
    p.ChangeFrequency(Re); time.sleep(0.5)
    p.ChangeFrequency(Mi); time.sleep(0.5)
    p.ChangeFrequency(Mi); time.sleep(0.5)
    p.ChangeFrequency(Mi)
    p.stop()

def song3():  # SW3 눌렀을 때 재생
    p.start(50)
    p.ChangeFrequency(Fa); time.sleep(0.5)
    p.ChangeFrequency(Mi); time.sleep(0.5)
    p.ChangeFrequency(Re); time.sleep(0.5)
    p.ChangeFrequency(Do); time.sleep(0.5)
    p.stop()

def song4():  # SW4 눌렀을 때 재생
    p.start(50)
    p.ChangeFrequency(Sol); time.sleep(0.5)
    p.ChangeFrequency(Mi);  time.sleep(0.5)
    p.ChangeFrequency(Do);  time.sleep(0.5)
    p.ChangeFrequency(Mi);  time.sleep(0.5)
    p.ChangeFrequency(Sol); time.sleep(0.5)
    p.stop()

# 메인 루프 -----------------------------------------------------------
try:
    while True:
        # 각 스위치 상태 읽기 (1: 눌림, 0: 안눌림)
        SW1Status = GPIO.input(SW1)
        SW2Status = GPIO.input(SW2)
        SW3Status = GPIO.input(SW3)
        SW4Status = GPIO.input(SW4)

        # 스위치에 따라 대응하는 노래 재생
        if SW1Status == 1:
            song1()
        elif SW2Status == 1:
            song2()
        elif SW3Status == 1:
            song3()
        elif SW4Status == 1:
            song4()

except KeyboardInterrupt:
    # Ctrl+C 눌러 종료할 때 예외 처리
    pass
