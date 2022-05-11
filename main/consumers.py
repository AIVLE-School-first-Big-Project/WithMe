import json
from channels.generic.websocket import WebsocketConsumer
from .predict import predict_neck, predict_eyes
from timer.models import TimeLog, UserLog
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from django.utils import timezone

EXIST_STATE = dict()


class PredictConsumer(WebsocketConsumer):
    def __init__(self):
        super().__init__(self)
        self.eyes_list = []
        self.exist_list = []
        self.eyes_cnt = 0
        self.user_log_id = ''

    def connect(self):
        global EXIST_STATE
        self.user_log_id = self.scope['url_route']['kwargs']['user_log']
        EXIST_STATE[self.user_log_id] = 0
        self.accept()

    def disconnect(self, close_code):
        item = UserLog.objects.get(id=self.user_log_id)
        item.end_time = timezone.now()
        item.save()

    # Receive message from WebSocket
    def receive(self, text_data):
        global EXIST_STATE
        text_data_json = json.loads(text_data)
        type = text_data_json['type']

        if type == 'ST':
            item = UserLog.objects.get(id=self.user_log_id)
            if item.end_time is None:
                self.send(text_data=json.dumps({
                    'type': 'on'
                }))
            else:
                self.send(text_data=json.dumps({
                    'type': 'dis'
                }))
            return
        message = text_data_json['message']
        if type == 'DE':  # DetectEyes
            self.eyes_cnt += 1

            res = predict_eyes(message)
            self.eyes_list.append(res[0])
            self.exist_list.append(res[1])

            if self.eyes_cnt >= 2:
                self.eyes_cnt, res = 0, 0

                if sum(self.eyes_list) >= 2:
                    res = 1
                if sum(self.exist_list) >= 2:
                    EXIST_STATE[self.user_log_id] = 1
                    res = 2
                else:
                    EXIST_STATE[self.user_log_id] = 0

                self.eyes_list.clear()
                self.exist_list.clear()

                # db event save
                prev_item = TimeLog.objects.filter(
                    Q(user_log_id=self.user_log_id)
                ).first()
                prev = prev_item.event_type

                if prev != res:
                    curr = TimeLog(user_log_id=self.user_log_id, event_type=res)
                    curr.save()
                    item = UserLog.objects.get(id=self.user_log_id)
                    if prev != 0 and res == 0:
                        parsed_t = parse_datetime(str(prev_item.time))
                        parsed_t2 = parse_datetime(str(curr.time))
                        time_value = int((parsed_t2 - parsed_t).total_seconds())
                        item.abnormal_time += time_value
                        item.save()
                    self.send(text_data=json.dumps({
                        'type': 'res_eyes',
                        'message': res,
                        'abnormal': item.abnormal_time,
                    }))


class PredictConsumer2(WebsocketConsumer):
    def __init__(self):
        super().__init__(self)
        self.neck_list = []
        self.neck_cnt = 0
        self.exist_state = 0
        self.user_log_id = ''

    def connect(self):
        self.user_log_id = self.scope['url_route']['kwargs']['user_log']
        self.accept()

    def disconnect(self, close_code):
        del (dict[self.user_log_id])

    # Receive message from WebSocket
    def receive(self, text_data):
        global EXIST_STATE
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']

        if type == 'DN':  # DetectNeck
            if EXIST_STATE[self.user_log_id] == 1:
                pass
            else:
                self.neck_cnt += 1
                res = predict_neck(message)
                self.send(text_data=json.dumps({
                    'type': 'res_neck',
                    'message': res,
                }))

                self.neck_list.append(res)
                # 10초 마다 저장
                if self.neck_cnt > 4:
                    self.neck_cnt, res = 0, 0
                    sum_value = sum(self.neck_list)
                    self.neck_list.clear()

                    item = UserLog.objects.get(id=self.user_log_id)
                    item.textneck_point += sum_value
                    item.save()
