# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np

# 경로 설정
BASE_DIR = os.path.dirname(__file__)
INPUT_DIR = os.path.join(BASE_DIR, "..", "img")
IMG_NAMES = [f"{i}.jpg" for i in range(1, 5)]

# 파라미터 설정
TARGET_WIDTH = 960  # 이미지 가로 크기 통일

# 노란색 HSV 범위
YELLOW_LOWER = np.array([15, 70, 70], dtype=np.uint8)
YELLOW_UPPER = np.array([35, 255, 255], dtype=np.uint8)

# 형태학 커널
K_OPEN  = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
K_CLOSE = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))

# 비율 유지하며 이미지 크기 조정
def resize_keep_aspect(img, target_width):
    h, w = img.shape[:2]
    if w == 0:
        return img
    scale = target_width / float(w)
    new_w = target_width
    new_h = int(round(h * scale))
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

# 노란색만 남기고 나머지는 검정 처리
def extract_yellow_only(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)                     # BGR → HSV 변환
    mask = cv2.inRange(hsv, YELLOW_LOWER, YELLOW_UPPER)            # 노란색 영역 마스크
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  K_OPEN,  1)     # 작은 노이즈 제거
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, K_CLOSE, 1)     # 끊긴 영역 연결
    result = cv2.bitwise_and(bgr, bgr, mask=mask)                  # 노란색만 남기기
    return result

def main():
    cv2.namedWindow("Yellow Lane Only (ESC to quit)", cv2.WINDOW_NORMAL)

    for name in IMG_NAMES:
        path = os.path.join(INPUT_DIR, name)
        img = cv2.imread(path)                                     # 이미지 읽기
        if img is None:
            print(f"[경고] 이미지 읽기 실패: {path}")
            continue

        img = resize_keep_aspect(img, TARGET_WIDTH)                # 크기 조정
        yellow_only = extract_yellow_only(img)                     # 노란색만 추출

        cv2.imshow("Yellow Lane Only (ESC to quit)", yellow_only)  # 결과 출력
        key = cv2.waitKey(0) & 0xFF
        if key == 27:  # ESC 키
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()