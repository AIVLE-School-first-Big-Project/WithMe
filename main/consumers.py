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

    def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['user_log']
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        item = UserLog.objects.filter(Q(id=self.room_group_name) & Q(end_time__isnull=False))
        if len(item):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'dis',
                }
            )

        self.accept()

    def disconnect(self, close_code):
        item = UserLog.objects.filter(Q(id=self.room_group_name) & Q(end_time__isnull=True))
        if len(item):
            item[0].end_time = timezone.now()
            item[0].save()
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        type = text_data_json['type']

        if type == 'DE': # DetectEyes
            self.eyes_cnt += 1

            res = predict_eyes(message)
            self.eyes_list.append(res[0])
            self.exist_list.append(res[1])

            if self.eyes_cnt >= 10:
                self.eyes_cnt, res = 0, 0

                if sum(self.eyes_list) >= 6:
                    res = 1
                if sum(self.exist_list) >= 6:
                    res = 2

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
            self.neck_cnt += 1

            res = predict_neck(message)
            self.neck_list.append(res)

            if self.neck_cnt >= 10:
                prev_item = TimeLog.objects.all().filter(
                    Q(user_log_id=self.room_group_name)
                ).first()
                prev = prev_item.event_type
                if prev == 2:
                    pass
                else:
                    self.neck_cnt, res = 0, 0
                    sum_value = sum(self.neck_list)
                    # db event save
                    item = UserLog.objects.get(id=self.room_group_name)
                    item.textneck_point += sum_value
                    item.save()
                    self.neck_list.clear()
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'res_neck',
                            'message': sum_value,
                            'neckpoint': item.textneck_point,
                        }
                    )


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
        neckpoint = args['neckpoint']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'res_neck',
            'message': message,
            'neckpoint': neckpoint,
        }))

    # Receive message from room group
    def disconnection(self):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'dis'
        }))