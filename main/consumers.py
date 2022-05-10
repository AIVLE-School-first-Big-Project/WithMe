# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .predict import *
from timer.models import TimeLog, UserLog
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from django.utils import timezone
import datetime

class ChatConsumer(WebsocketConsumer):
    def __init__(self):
        super().__init__(self)
        self.eyes_list = []
        self.exist_list = []
        self.neck_list = []
        self.eyes_cnt = 0
        self.neck_cnt = 0
        self.exist_state = 0

    def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['user_log']
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()

    def disconnect(self, close_code):
        item = UserLog.objects.get(id=self.room_group_name)
        item.end_time = timezone.now()
        item.save()
        print(item.end_time)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']

        if type == 'ST':
            item = UserLog.objects.get(id=self.room_group_name)
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
        if type == 'DE': # DetectEyes
            self.eyes_cnt += 1

            res = predict_eyes(message)
            self.eyes_list.append(res[0])
            self.exist_list.append(res[1])

            if self.eyes_cnt >= 2:
                self.eyes_cnt, res = 0, 0

                if sum(self.eyes_list) >= 2:
                    res = 1
                if sum(self.exist_list) >= 2:
                    self.exist_state = 1
                    res = 2
                else:
                    self.exist_state = 0

                self.eyes_list.clear()
                self.exist_list.clear()

                # db event save
                prev_item = TimeLog.objects.all().filter(
                    Q(user_log_id=self.room_group_name)
                ).first()
                prev = prev_item.event_type

                if prev != res:
                    curr = TimeLog(user_log_id=self.room_group_name, event_type=res)
                    curr.save()
                    item = UserLog.objects.get(id=self.room_group_name)
                    if prev != 0 and res == 0:
                        parsed_t = parse_datetime(str(prev_item.time))
                        parsed_t2 = parse_datetime(str(curr.time))
                        time_value = int((parsed_t2 - parsed_t).total_seconds())
                        item.abnormal_time += time_value
                        item.save()

                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'res_eyes',
                            'message': res,
                            'abnormal': item.abnormal_time,
                        }
                    )

        elif type == 'DN': # DetectNeck
            if self.exist_state == 1:
                pass
            else:
                self.neck_cnt += 1
                res = predict_neck(message)
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'res_neck',
                        'message': res,
                    }
                )
                self.neck_list.append(res)
                # 10초 마다 저장
                if self.neck_cnt > 9:
                    self.neck_cnt, res = 0, 0
                    sum_value = sum(self.neck_list)
                    self.neck_list.clear()

                    item = UserLog.objects.get(id=self.room_group_name)
                    item.textneck_point += sum_value
                    item.save()


    # Receive message from room group
    def res_eyes(self, args):
        message = args['message']
        abnormal = args['abnormal']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'res_eyes',
            'message': message,
            'abnormal': abnormal,
        }))

    def res_neck(self, args):
        message = args['message']
        self.send(text_data=json.dumps({
            'type': 'res_neck',
            'message': message,
        }))