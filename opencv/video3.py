# mtcnn을 이용한 얼굴 검출
# https://github.com/ipazc/mtcnn
# pip install mtcnn tensorflow

from mtcnn import MTCNN
import cv2

detector = MTCNN()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    height, width = frame.shape[:2]

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faces = detector.detect_faces(img)
    for face in faces:
        x = face['box'][0]
        y = face['box'][1]
        w = face['box'][2]
        h = face['box'][3]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.line(frame, face['keypoints']['left_eye'], face['keypoints']['left_eye'], (0, 0, 255), 10)
        cv2.line(frame, face['keypoints']['right_eye'], face['keypoints']['right_eye'], (0, 0, 255), 10)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
