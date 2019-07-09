from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from kombu.utils import json

from .models import Comments
from .models import UploadImage


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)

        post_id = self.scope['url_route']['kwargs']['post_id']

        comments = list(Comments.objects.filter(post_id=post_id, visible=True).order_by('-pub_date').values('id', 'owner', 'comment'))

        chat_room = post_id
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name,
        )

        await self.send({
            'type': 'websocket.accept',
        })

        await self.send({
            'type': 'websocket.send',
            'text': json.dumps(comments)
        })

    async def websocket_receive(self, event):
        print('receive', event)
        post_id = self.scope['url_route']['kwargs']['post_id']
        front_text = event.get('text', None)
        if front_text is not None:
            print(front_text)
            loaded_dic_date = json.loads(front_text)
            type = loaded_dic_date.get('type', None)
            print('type', type)
            writed_comment = loaded_dic_date.get('message', None)
            edited_comment = loaded_dic_date.get('new_comment', None)
            edited_comment_id = loaded_dic_date.get('comment_id', None)
            if type == 'new_comment':
                print('writing new one')
                user = self.scope['session']['email']
                user_id = User.objects.get(username=user).pk

                my_response = {
                    'comment': writed_comment,
                    'owner': user_id
                }

                await self.create_comment_object(writed_comment)

                await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        'type': 'chat_message',
                        'text': json.dumps(my_response)
                    }
                )

            elif type == 'editing_comment':
                print('editing')
                edited_comment_obj = Comments.objects.get(id=edited_comment_id)
                edited_comment_obj.comment = edited_comment
                edited_comment_obj.save()

                comments = list(Comments.objects.filter(post_id=post_id, visible=True).order_by('-pub_date').values('id', 'owner', 'comment'))

                await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        'type': 'chat_message',
                        'text': json.dumps(comments)
                    }
                )

            elif type == 'deleting_comment':
                print('deleting')
                edited_comment_obj = Comments.objects.get(id=edited_comment_id)
                edited_comment_obj.visible = False
                edited_comment_obj.save()

                comments = list(Comments.objects.filter(post_id=post_id, visible=True).order_by('-pub_date').values('id', 'owner', 'comment'))

                await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        'type': 'chat_message',
                        'text': json.dumps(comments)
                    }
                )

    async def chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def websocket_disconnect(self, event):
        print('disconnect', event)

    @database_sync_to_async
    def create_comment_object(self, comment):
        username = self.scope['session']['email']
        user = User.objects.get(username=username)
        post_id = self.scope['url_route']['kwargs']['post_id']
        post = UploadImage.objects.get(pk=post_id)
        return Comments.objects.create(owner=user, post=post, comment=comment)
