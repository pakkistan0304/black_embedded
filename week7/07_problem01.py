# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# 스위치 핀 번호 (BCM 모드 기준)
SW1 = 5
SW2 = 6
SW3 = 13
SW4 = 19

# 각 스위치가 눌린 횟수를 저장하는 변수
SW1Value = 0
SW2Value = 0
SW3Value = 0
SW4Value = 0

# 직전 클릭 상태 저장 (눌림 → 뗌 판별용)
sw1lastClick = 0
sw2lastClick = 0
sw3lastClick = 0
sw4lastClick = 0

# GPIO 설정
GPIO.setwarnings(False)          # 불필요한 경고 메시지 비활성화
GPIO.setmode(GPIO.BCM)           # BCM 핀 번호 체계 사용
# 각 스위치를 입력으로 설정, 내부 풀다운 저항 활성화
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        # 각 스위치의 현재 입력 상태 읽기 (1=눌림, 0=뗌)
        sw1Click = GPIO.input(SW1)
        sw2Click = GPIO.input(SW2)
        sw3Click = GPIO.input(SW3)
        sw4Click = GPIO.input(SW4)

        # SW1 눌림 감지 (0→1 상승 엣지)
        if sw1Click == 1 and sw1lastClick == 0:
            sw1lastClick = 1
            SW1Value += 1
            print('SW1 click ' + str(SW1Value))
        elif sw1Click == 0:
            sw1lastClick = 0

        # SW2 눌림 감지
        if sw2Click == 1 and sw2lastClick == 0:
            sw2lastClick = 1
            SW2Value += 1
            print('SW2 click ' + str(SW2Value))
        elif sw2Click == 0:
            sw2lastClick = 0

        # SW3 눌림 감지
        if sw3Click == 1 and sw3lastClick == 0:
            sw3lastClick = 1
            SW3Value += 1
            print('SW3 click ' + str(SW3Value))
        elif sw3Click == 0:
            sw3lastClick = 0

        # SW4 눌림 감지
        if sw4Click == 1 and sw4lastClick == 0:
            sw4lastClick = 1
            SW4Value += 1
            print('SW4 click ' + str(SW4Value))
        elif sw4Click == 0:
            sw4lastClick = 0

except KeyboardInterrupt:
    # Ctrl+C 누르면 루프 종료
    pass
