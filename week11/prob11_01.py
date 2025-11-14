import cv2 as cv
import numpy as np
import threading, time
import SDcar 

# 기본 주행 속도 및 연산 중 0 division 방지를 위한 epsilon
speed = 35
epsilon = 0.0001

def func_thread():
    # 별도 쓰레드에서 동작하는 간단한 alive 체크 루프
    i = 0
    while True:
        print("alive!!")
        time.sleep(1)
        i += 1
        if is_running is False:
            break

def key_cmd(which_key):
    is_exit = False
    global enable_linetracing

    if which_key & 0xFF == 82:        # UP
        print('up')
        car.motor_go(speed)
    elif which_key & 0xFF == 84:      # DOWN
        print('down')
        car.motor_back(speed)
    elif which_key & 0xFF == 81:      # LEFT
        print('left')
        car.motor_left(speed)
    elif which_key & 0xFF == 83:      # RIGHT
        print('right')
        car.motor_right(speed)
    elif which_key & 0xFF == 32:      # SPACE - stop
        car.motor_stop()
        print('stop')
    elif which_key & 0xFF == ord('q'):
        # 프로그램 종료 요청
        car.motor_stop()
        print('exit')
        is_exit = True
    elif which_key & 0xFF == ord('e'):
        # 라인트레이싱 활성화
        enable_linetracing = True
        print('enable_linetracing:', enable_linetracing)
    elif which_key & 0xFF == ord('w'):
        # 라인트레이싱 비활성화
        enable_linetracing = False
        car.motor_stop()
        print('enable_linetracing 2:', enable_linetracing)
    return is_exit

def detect_maskY_BGR(frame):
    """
    BGR 색공간에서 노란색 성분 추출을 위한 단순 Y 마스크 계산.
    B,G,R 채널의 비율을 통해 노란색 정도를 계산한 뒤 threshold 적용.
    """
    B = frame[:,:,0]
    G = frame[:,:,1]
    R = frame[:,:,2]

    # Y 성분 단순 계산 (튜닝 필요)
    Y = G*0.5 + R*0.5 - B*0.7
    Y = Y.astype(np.uint8)

    # 노이즈 제거용 블러
    Y = cv.GaussianBlur(Y, (5,5), cv.BORDER_DEFAULT)

    # Thresholding (튜닝 필요)
    _, mask_Y = cv.threshold(Y, 100, 255, cv.THRESH_BINARY)
    return mask_Y

def show_grid(img):
    """
    화면을 10등분한 x-grid 선을 그려 moment 위치 파악을 돕는 시각 보조선
    """
    h, _, _ = img.shape
    for x in v_x_grid:
        cv.line(img, (x, 0), (x, h), (0,255,0), 1, cv.LINE_4)

def line_tracing(cx):
    """
    라인트레이싱 제어 로직.
    이전 3개의 moment 값 평균을 사용해 안정성 확보.
    cx = 현재 centroid x좌표
    """
    global moment
    global v_x

    tolerance = 0.1
    diff = 0

    # moment 3개가 유효한 경우에만 계산
    if moment[0] != 0 and moment[1] != 0 and moment[2] != 0:
        avg_m = np.mean(moment)
        diff = np.abs(avg_m - cx) / v_x

    print('diff = {:.4f}'.format(diff))

    # moment 변화량이 허용 범위 이내인 경우
    if diff <= tolerance:

        # 이전 moment 업데이트
        moment[0] = moment[1]
        moment[1] = moment[2]
        moment[2] = cx

        # 좌표 범위에 따라 주행 방향 결정
        if v_x_grid[2] <= cx < v_x_grid[3]:
            car.motor_go(speed)
            print('go')
        elif v_x_grid[3] <= cx:
            car.motor_left(speed)
            print('turn left')
        elif v_x_grid[1] <= cx:
            car.motor_right(speed)
            print('turn right')

    else:
        # 갑작스러운 변화 → 직진 후 moment 초기화
        car.motor_go(speed)
        print('go')
        moment = [0,0,0]

def main():
    # 카메라 초기화
    camera = cv.VideoCapture(0)
    camera.set(cv.CAP_PROP_FRAME_WIDTH, v_x)
    camera.set(cv.CAP_PROP_FRAME_HEIGHT, v_y)

    try:
        while camera.isOpened():
            # 프레임 획득
            ret, frame = camera.read()
            if not ret:
                break

            cv.imshow('camera', frame)

            # 영상 아래쪽 부분만 crop
            crop_img = frame[180:,:]

            # 노란색 마스크 추출
            maskY = detect_maskY_BGR(crop_img)

            # Contour 검색
            contours, _ = cv.findContours(maskY, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            if len(contours) > 0:
                # 가장 큰 contour 선택
                c = max(contours, key=cv.contourArea)
                m = cv.moments(c)

                # centroid 계산
                cx = int(m['m10']/(m['m00']+epsilon))
                cy = int(m['m01']/(m['m00']+epsilon))

                cv.circle(crop_img, (cx,cy), 3, (0,0,255), -1)
                cv.drawContours(crop_img, contours, -1, (0,255,0), 3)
                cv.putText(crop_img, str(cx), (10, 10), cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0))

                # 라인트레이싱 모드일 때 라인트레이싱 수행
                if enable_linetracing:
                    line_tracing(cx)

            # 보조 grid 표시
            show_grid(crop_img)

            # crop 이미지를 2배 확대 출력
            cv.imshow('crop_img ', cv.resize(crop_img, dsize=(0,0), fx=2, fy=2))

            # 키 입력 처리
            which_key = cv.waitKey(20)
            is_exit = False
            if which_key > 0:
                is_exit = key_cmd(which_key)
            if is_exit:
                cv.destroyAllWindows()
                break

    except Exception as e:
        print(e)
        global is_running
        is_running = False

if __name__ == '__main__':

    # 카메라 해상도 및 grid 계산
    v_x = 320
    v_y = 240
    v_x_grid = [int(v_x*i/10) for i in range(1, 10)]

    # moment 초기값
    moment = np.array([0, 0, 0])

    print(v_x_grid)

    # 쓰레드 시작
    t_task1 = threading.Thread(target=func_thread)
    t_task1.start()

    # 자동차 제어 객체
    car = SDcar.Drive()

    is_running = True
    enable_linetracing = False
    main()

    # 종료 시 GPIO 해제
    is_running = False
    car.clean_GPIO()
    print('end vis')