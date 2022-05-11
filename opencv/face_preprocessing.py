import cv2
import mediapipe as mp
import itertools


def getEyes_mediapipe_mesh(image):
    mp_face_mesh = mp.solutions.face_mesh

    # 사용자가 이미지를 바라봤을 때 왼쪽 눈(이미지 입장에서 오른쪽 눈)
    left_index = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LEFT_EYE)))
    right_index = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_EYE)))

    with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5,
                               min_tracking_confidence=0.5) as face_mesh:
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # x, y 모든 좌표값은 normalized 되어있음(min-max scale 한 것으로 추정됨)
                left_x_list = [face_landmarks.landmark[i].x for i in left_index]
                left_y_list = [face_landmarks.landmark[i].y for i in left_index]

                right_x_list = [face_landmarks.landmark[i].x for i in right_index]
                right_y_list = [face_landmarks.landmark[i].y for i in right_index]

                # scale을 원래 값으로 돌리기 위해 최댓값구하기
                max_x = image.shape[1]
                max_y = image.shape[0]

                left_x, left_y, left_w, left_h = get_boundary_box(left_x_list, left_y_list, max_x, max_y)
                right_x, right_y, right_w, right_h = get_boundary_box(right_x_list, right_y_list, max_x, max_y)

                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                left_eye_img = image[left_x: left_x + left_w, left_y: left_y + left_h]
                right_eye_img = image[right_x: right_x + right_w, right_y: right_y + right_h]

                cv2.imwrite('저장할 폴더/img이름.jpeg', left_eye_img)
                cv2.imwrite('저장할 폴더/img이름.jpeg', right_eye_img)


def get_boundary_box(x_list, y_list, max_x, max_y):
    x_start = min(x_list) * max_x  # image.shape[1]
    y_start = min(y_list) * max_y  # image.shape[0]

    x_end = max(x_list) * max_x
    y_end = max(y_list) * max_y

    print(f'start coord: ({x_start, y_start}), end coord: ({x_end, y_end})')

    # boundary box에 여분을 두기 위해 거리 구하기
    x_dist = int((x_end - x_start) // 2)
    y_dist = int(y_end - y_start)

    # boundary box start x
    x = int(x_start - x_dist)

    # boundary box start y
    y = int(y_start - y_dist)

    # boundary box width
    w = int(x_end + x_dist - x)

    # boundary box height
    h = int(y_end + y_dist - y)

    return x, y, w, h
