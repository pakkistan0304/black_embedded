import cv2

# 얼굴 및 눈 검출용 Haar Cascade 분류기 불러오기
# cv2.data.haarcascades는 OpenCV 설치 경로에 포함된 haarcascade 폴더의 경로를 자동으로 반환함
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

# XML 파일이 정상적으로 로드되지 않은 경우 프로그램 종료
if face_cascade.empty() or eye_cascade.empty():
    print("Failed to load Haar cascades")
    raise SystemExit

# 기본 카메라(0번 장치)에서 영상 입력 받기
cap = cv2.VideoCapture(0)   # 리눅스에서는 /dev/video0
if not cap.isOpened():
    print("Cannot open camera")
    raise SystemExit

while True:
    # 프레임 단위로 영상 읽기
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?)")
        break

    # 영상 데이터를 흑백(그레이스케일)으로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 얼굴 검출 (scaleFactor: 이미지 크기 축소 비율, minNeighbors: 검출 신뢰도)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60)
    )

    # 검출된 얼굴마다 사각형 표시
    for (x, y, w, h) in faces:
        # 얼굴 영역에 파란색(255,0,0) 사각형 표시
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # 얼굴 영역만 잘라서 눈 검출 수행
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # 눈 검출 (얼굴 영역 내부에서만 검색)
        eyes = eye_cascade.detectMultiScale(
            roi_gray, scaleFactor=1.15, minNeighbors=5, minSize=(20, 20)
        )

        # 검출된 눈마다 초록색(0,255,0) 사각형 표시
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    # 결과 영상 출력 (q를 누르면 종료)
    cv2.imshow("face+eye (press q to quit)", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 카메라 및 창 닫기
cap.release()
cv2.destroyAllWindows()