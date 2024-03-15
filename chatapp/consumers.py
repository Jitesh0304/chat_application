import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
from .models import Group, Chat
from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async



# class MyJsonWebsocketConsumer(JsonWebsocketConsumer):

#     def connect(self):
#         print("Websocket connected .....")
#         # print(self.scope)
#         self.group_name = self.scope['url_route']['kwargs']['groupname']
#         self.accept()       ## accept the connection request
#         # self.close()      ## whenever you want to reject or forcefully close the connection .. you can mention this
#         ## Or add a custom WebSocket error code!
#         # self.close(code=4123)
#         async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)


#     def receive_json(self, content, **kwargs):
#         # print(type(content))
#         # print(content)
#         message = content
#         # print(self.scope['user'])
#         if self.scope['user'].is_authenticated:
#             group_data = Group.objects.get(name= self.group_name)

#             message['user'] = self.scope['user'].username
#             new_chat = Chat(
#                 content= message['msg'],
#                 group = group_data
#             )
#             new_chat.save()

#             # print(type(message))
#             async_to_sync(self.channel_layer.group_send)(self.group_name,{
#                                                                         'type': 'chat.message',
#                                                                         'message': message,
#                                                                     }
#                                                                 )
#             # print("Message received from client .....", text_data)
#             # self.send(text_data= "Hello")
#             ## we can send binary data 
#             # self.send(bytes_data= data)
#         else:
#             self.send_json(content= {'msg':'Login required'})


#     def chat_message(self, event):
#         message = event['message']
#         self.send_json(content=message)
#         # self.send(text_data=json.dumps({'msg':message}))




#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
#         print("Websocket disconnected .....", close_code)
#         raise StopConsumer()





class MyAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    # groups = ["broadcast"]

    async def connect(self):
        print("Websocket connected .....")

        self.group_name = self.scope['url_route']['kwargs']['groupname']
        ## Called on connection.
        ## To accept the connection call:
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        ## Or accept the connection and specify a chosen subprotocol.
        ## A list of subprotocols specified by the connecting client
        ## will be available in self.scope['subprotocols']
        # await self.accept("subprotocol")
        ## To reject the connection, call:
        # await self.close()

    async def receive_json(self, content, **kwargs):
        print("Message received from client .....", content)

        receive_message = content

        if self.scope['user'].is_authenticated:
            receive_message['user'] = self.scope['user'].username
            group_data = await database_sync_to_async(Group.objects.get)(name=self.group_name)

            new_chat = Chat(content= receive_message['msg'], group=group_data, senduser=self.scope['user'])
            await database_sync_to_async(new_chat.save)()

            await self.channel_layer.group_send(self.group_name, {
                                                'type':'chat.message',
                                                'message': receive_message
                                            })
            
        else:
            await self.send_json(content= {'msg':'Login required'})
        

    async def chat_message(self, event):
        message = event['message']
        await self.send_json(content= message)
        ## Called with either text_data or bytes_data for each frame
        ## You can call:
        ## Or, to send a binary frame:
        # await self.send(bytes_data="Hello world!")
        ## Want to force-close the connection? Call:
        # await self.close()
        ## Or add a custom WebSocket error code!
        # await self.close(code=4123)

    async def disconnect(self, close_code):
        ## Called when the socket closes
        print("Websocket disconnected .....", close_code)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        StopConsumer()