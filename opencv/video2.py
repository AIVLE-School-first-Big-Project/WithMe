# face_recognition을 이용한 얼굴 검출
# https://github.com/ageitgey/face_recognition/blob/master/examples/digital_makeup.py
# 설치 필요 pakage
# Cmake, dlib, face_recognition, opencv-python

# CMake 설치 경로 : https://cmake.org/download/
# dlib 설치 경로 : https://updaun.tistory.com/entry/python-python-37-dlib-install-error
# 1. .whl파일을 다운 후 프롬프트에서 파일 위치로 이동
# 2. pip install dlib~~~.whl 파일 실행

# face_recognition 설치
# pip install face_recognition
# pip install --no-dependencies face_recognition (위의 명령어가 안 될 시 사용)

import face_recognition
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
process_this_frame = True
while True:
    ret, frame = cap.read()

    small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_landmark_list = face_recognition.face_landmarks(rgb_small_frame)
        

        face_name=[]
        for face_encoding in face_encodings:
            face_name.append("Unknown")

    
    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_name):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom-35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255,255,255), 1)

    for fl in face_landmark_list:
        array_left = np.array(fl['left_eye'])*4
        array_right = np.array(fl['right_eye'])*4
        cv2.polylines(frame, [array_left], True, (255, 0, 0), 5)
        cv2.polylines(frame, [array_right], True, (255, 0, 0), 5)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()