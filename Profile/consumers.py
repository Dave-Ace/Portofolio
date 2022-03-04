import json
from asgiref.sync import async_to_sync
from asyncio import sleep
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from User.models import Message, User


class ChatConsumer(WebsocketConsumer):    
    def fetch_messages(self, data):
        author = data['from']
        to = data['to']
        
        messages_to = Message.objects.filter(author=author, to=to).order_by('-timestamp').all()[:10]
        messages_from = Message.objects.filter(author=to, to=author).order_by('-timestamp').all()[:10]
        
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages_to, messages_from)
        }
        self.send_message(content)

    def messages_to_json(self, messages_to, messages_from):
        result = []
        x = messages_to.count()
        y = messages_from.count()
        
        me_to = []
        me_from = []
        for message in messages_to:
            me_to.append(message)
        for message in messages_from:
            me_from.append(message)

        messages_from = []
        messages_to  = []
        
        for i in me_to:
            messages_to.append(me_to[x-1])
            x -= 1
        
        for i in me_from:
            messages_from.append(me_from[y-1])
            y -= 1

        while len(messages_from) > 0:
            for message in messages_to:
                for message2 in messages_from:
                    if messages_to.index(message) == len(messages_to)-1 and message.timestamp == "appended":
                        result.append(self.message_to_json(message2))
                        messages_from.remove(message2)
                    elif message.timestamp=="appended":
                        break
                    else:
                        if message.timestamp < message2.timestamp and message.timestamp:
                            if message in result:
                                break
                            else:
                                result.append(self.message_to_json(message))
                                message.timestamp = "appended"
                                break
                        elif message.timestamp == message2.timestamp:
                            break
                        else:
                            if message2 in result:
                                break
                            else:
                                result.append(self.message_to_json(message2))
                                messages_from.remove(message2)
                                continue
        
        if len(messages_to) != 0:
            for message in messages_to:
                if message.timestamp != "appended":
                    result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return{
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    def new_message(self, data):
        author = data['from']
        print(author)
        to = data['to']
        
        author_user = User.objects.filter(username=author)[0]
        message = Message.objects.create(
            author=author_user, 
            content=data['message'],
            to=User.objects.get(id=to))
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }
    
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)
    
    def send_chat_message(self, message):

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

class TimeConsumer(AsyncWebsocketConsumer):
    async def connect(self):        
        await self.accept()
        for i in range(6):
            if (i == 5):
                await self.send(json.dumps({'message': "{% static 'css/style-green.css' %}" }))
                await sleep(1)
            elif i == 0:
                await self.send(json.dumps({'message': "{% static 'css/style.css' %}" }))
                await sleep(1)
            else:
                await self.send(json.dumps({'message': i }))
                await sleep(1)