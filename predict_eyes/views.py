from django.shortcuts import render
import mediapipe as mp
import itertools
import numpy as np
import matplotlib.pyplot as plt
import cv2
import base64
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import logging

# for image capture
from django.views.decorators.csrf import csrf_exempt
from keras.models import load_model
import os
from withme.settings import MEDIA_ROOT

logger = logging.getLogger(__name__)
model_eye = load_model(os.path.join(MEDIA_ROOT, 'mobileNet_v3_for_small_eyes.h5'))
model_neck = load_model(os.path.join(MEDIA_ROOT, 'mobileNet_v3_turtleNeck.h5'))

def extractData(request):
    search = 'base64,'
    data = request.POST.__getitem__('data')
    index = data.find(search) + len(search)
    return data[index:]

@csrf_exempt
def detectme2(request):
	if request.POST:
		data = extractData(request)

		left_eye, right_eye = getEyes_mediapipe_mesh(base64.b64decode(data))

		user_state = 0 if left_eye + right_eye <= 0.5 else 1
		user_exist_state = 0 if left_eye == -1 else 1

		answer = {
            'userAwakeState': str(user_state),
            'userExistState': str(user_exist_state),
            'left eye' : str(left_eye),
            'right eye' : str(right_eye),
            }
		return JsonResponse(answer)
	return render(request, 'predict_eyes/capture_video.html')


@csrf_exempt
def detectneck(request):
	if request.POST:
		data = extractData(request)

		y_pred = getTurtle_mediapipe_mesh(base64.b64decode(data))

    # 0: abnormal 1: normal
		neck_state = 0 if y_pred < 0.5 else 1

		answer = {
            'userNeckState': str(neck_state),
            'userNeckpred': str(y_pred),
            }
		return JsonResponse(answer)
	return render(request, 'predict_eyes/capture_video.html')


def getTurtle_mediapipe_mesh(image):
  encoded_img = np.fromstring(image, dtype = np.uint8)
  image = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  image = image/255
  image = cv2.resize(image, (224, 224))
  image = np.expand_dims(image, axis=0)

  y_pred = np.squeeze(model_neck.predict(image))
  return y_pred

def getEyes_mediapipe_mesh(image):
    # mp_drawing = mp.solutions.drawing_utils
    encoded_img = np.fromstring(image, dtype = np.uint8)
    image = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    # print(image.shape)

    mp_face_mesh = mp.solutions.face_mesh

    # 이미지 입장에서 왼쪽 눈(사람이 이미지를 봤을 땐 오른쪽에 있는 눈)
    left_index = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LEFT_EYE)))
    right_index = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_EYE)))

    #drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5,
                                min_tracking_confidence=0.5) as face_mesh:
        image.flags.writeable=False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        # image.flags.writeable = True
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
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
                #print(f'image shape: {image.shape}')

                #print('left eye')
                left_x, left_y, left_x2, left_y2 = get_boundary_box(left_x_list, left_y_list, max_x, max_y)
                #print('right eye')
                right_x, right_y, right_x2, right_y2 = get_boundary_box(right_x_list, right_y_list, max_x, max_y)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                left_eye_img = image[left_y: left_y2, left_x: left_x2]
                #print('left eye shape:', left_eye_img.shape)
                right_eye_img = image[right_y: right_y2, right_x: right_x2]
                #print('right eye shape:', right_eye_img.shape)

                # number = random.randrange(1, 10000)
                # cv2.imwrite(f'left_{number}.jpeg', left_eye_img)
                # cv2.imwrite(f'right_{number}.jpeg', right_eye_img)
                # plt.subplot(1,3,2)
                # plt.imshow(left_eye_img)
                # plt.show()

                # plt.subplot(1,3,3)
                # plt.imshow(right_eye_img)
                # plt.show()
                left_img = img_preprocessing(left_eye_img)
                right_img = img_preprocessing(right_eye_img)
                # print(left_img.shape)
                # print(right_img.shape)
                left_pred = model_eye.predict(left_img)[:, 0]
                right_pred = model_eye.predict(right_img)[:, 0]
                # print('left', left_pred)
                # print('right', right_pred)
                # print(left_pred, right_pred)
                return left_pred, right_pred
        else:
            return -1, -1



def img_preprocessing(img):
    img_resize = cv2.resize(img, (128, 128))
    # print('Reshaping', img_resize.shape)
    img_resize = img_resize.astype(np.float32)/255
    image = np.expand_dims(img_resize, axis=0)
    # print('add dim image shape:', image.shape)
    return image

def get_boundary_box(x_list, y_list, max_x, max_y):

    x_start = min(x_list) * max_x  # image.shape[1]
    y_start = min(y_list) * max_y  # image.shape[0]

    x_end = max(x_list) * max_x
    y_end = max(y_list) * max_y

    # print(f'start coord: ({x_start, y_start}), end coord: ({x_end, y_end})')

    # boundary box에 여분을 두기 위해 거리 구하기
    x_dist = int((x_end - x_start)//2)
    if x_dist == 0:
      x_dist = 10
    y_dist = int(y_end - y_start)
    if y_dist == 0:
      y_dist = 10

    # boundary box start x, end x, distance
    x = int(x_start - x_dist)
    x2 = int(x_end + x_dist)
    new_x_dist = x2 - x

    # boundary box start y, end y, distance
    y = int(y_start - y_dist)
    y2 = int(y_end + y_dist)
    new_y_dist = y2 - y

    # set same distance between x, x2 and y, y2
    if new_x_dist >= new_y_dist:
      dist = (new_x_dist - (y2-y))//2
      y -= dist
      y2 += dist
    else:
      dist = (new_y_dist - (x2-x))//2
      x -= dist
      x2 += dist

    # print(f'start coord ({x,y}) end coord ({x2, y2})')
    return x, y, x2, y2