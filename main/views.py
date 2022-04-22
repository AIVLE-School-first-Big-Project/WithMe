from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

# for image capture
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
import time


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

# for image capture
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    prev_time = 0
    FPS = 2
    
    while True:
        frame = camera.get_frame()
        
        current_time = time.time() - prev_time

        if (current_time > 1./ FPS) :            
            prev_time = time.time()

            # 이미지 저장 및 분석 코드

            
        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def detectme(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        print("에러입니다...")
        pass