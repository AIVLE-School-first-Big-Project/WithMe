import base64
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# for image capture
from django.views.decorators.csrf import csrf_exempt
import os, random
from withme.settings import MEDIA_ROOT

def index(request):
    if request.user.is_authenticated:
        return main(request)
    return render(request, "main/base_intro.html")

@login_required
def main(request):
    return render(request, "main/base_test.html")

@login_required
def settings(request):
    return render(request, "main/settings.html")

@csrf_exempt
def detectme(request):
    if request.POST:
        data = request.POST.__getitem__('data')
        data = data[22:] # data:image/png;base64 부분 제거
        number = random.randrange(1, 10000)

        # 저장 경로 및 파일명 설정
        filename = request.user.username + '_image_' + str(number) + '.png'
        save_path = os.path.join(MEDIA_ROOT, filename)

        image = open(save_path, "wb") # path+filename, "wb")
        image.write(base64.b64decode(data))
        image.close()

        # 모델 완성 시, 해당 result 반환
        number = random.randrange(1, 10000)
        user_state = '눈 뜨세요' if number % 2 else '화이팅 !!'
        answer = {
            'userState': user_state,
            'filepath' : save_path
            }

        return JsonResponse(answer)
    return render(request, 'main/video_test.html')