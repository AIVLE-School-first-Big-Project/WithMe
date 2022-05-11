# opencv의 haarcascade 모델을 이용한 얼굴 및 눈 검출
# 설치 필요 pakage
# opencv-python
# 다운로드 해야하는 모델
# model/ 아래 있음

import cv2

cap = cv2.VideoCapture(0)

face = cv2.CascadeClassifier('model/haarcascade_frontalface_alt2.xml')
leye = cv2.CascadeClassifier('model/haarcascade_lefteye_2splits.xml')
reye = cv2.CascadeClassifier('model/haarcascade_righteye_2splits.xml')

while True:
    ret, frame = cap.read()

    height, width = frame.shape[:2]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face.detectMultiScale(gray, minNeighbors=5, scaleFactor=1.05, minSize=(100, 100),
                                  flags=cv2.CASCADE_SCALE_IMAGE)

    cv2.rectangle(frame, (0, height - 50), (200, height), (0, 0, 0), thickness=cv2.FILLED)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 2)
        face_gray = gray[y:y + h, x:x + w]
        face_color = frame[y:y + h, x:x + w]

        left_eye = leye.detectMultiScale(face_gray, 1.1, 3)
        right_eye = reye.detectMultiScale(face_gray, 1.1, 3)

        for (ex, ey, ew, eh) in right_eye:
            cv2.rectangle(face_color, (ex, ey), (ex + ew, ey + eh), (255, 100, 100), 2)

        for (ex, ey, ew, eh) in left_eye:
            cv2.rectangle(face_color, (ex, ey), (ex + ew, ey + eh), (100, 100, 255), 2)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
