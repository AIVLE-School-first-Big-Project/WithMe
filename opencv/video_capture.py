import cv2
import os

from pathlib import Path

cap = cv2.VideoCapture(0)
isStart = False
classes, cnt = 0, 0
path = ['\\normal', '\\shoulder', '\\neck']
while True:
    ret, frame = cap.read()

    if isStart:
        if os.path.isdir(path[classes]):
            cv2.imwrite(path[classes] + f'\\img_{cnt}.jpg', frame)
        else:
            os.mkdir(path[classes])
            cv2.imwrite(path[classes] + f'\\img_{cnt}.jpg', frame)
        cnt += 1
        if cnt == 200:
            isStart = False
            cnt = 0
            classes += 1
            if classes >= len(path):
                cap.release()
                cv2.destroyAllWindows()
                break
    
    cv2.putText(frame, f'{path[classes]} : {cnt}', (10,20), 1, fontScale=1, color=(0,0,255), thickness=2)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) == 13:
        isStart = True
cap.release()
cv2.destroyAllWindows()