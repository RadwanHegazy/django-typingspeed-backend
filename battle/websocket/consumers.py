from channels.generic.websocket import WebsocketConsumer
from users.models import User
from battle.models import Battle
import json
from asgiref.sync import async_to_sync

class SearchBattle (WebsocketConsumer): 

    def connect(self):
        self.user:User = self.scope['user']
        
        self.accept()
        get_battle:dict = Battle.get_avaliable_battles(self.user)
    
        self.send(
            text_data=json.dumps(get_battle)
        )

        self.close()

    def disconnect(self, code):...

    def receive(self, text_data):...



class BattleConsumer (WebsocketConsumer) :
    
    def connect(self):
        self.user:User = self.scope['user']
        battle_id = self.scope['url_route']['kwargs']['battle_id']

        self.current_char_idx = 0
        
        try :
            self.battle = Battle.objects.get(id=battle_id)
        except Battle.DoesNotExist:
            self.close()
            return
        
        self.ROOM_GROUP = f"battle_{self.battle.id}"
        
        
        if self.user not in self.battle.users.all() :
            self.close()
            return
        
            
        
        self.accept()
        self.battle_body = self.battle.text   
        
        async_to_sync(self.channel_layer.group_add)(
            self.ROOM_GROUP,
            self.channel_name
        )

                    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.ROOM_GROUP,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        data_type = data['type']


        # check the char on the body of the battle
        if data_type == 'char' : 
            char = data['char']
            if self.current_char_idx == len(self.battle_body) - 1 :
                winner_txt = f'الفائز هو : {self.user.full_name}'

                async_to_sync(self.channel_layer.group_send)(
                    self.ROOM_GROUP,
                    {
                        'type' : 'win',
                        'event' : 
                            {
                                'type' : 'win',
                                'text' : winner_txt
                            }
                    }
               )

                self.user.points += 10
                self.user.save() 
                self.battle.winner = self.user
                self.battle.save()
                # close must be from front
                
            if self.battle_body[self.current_char_idx] == char:
                self.current_char_idx += 1

    def win (self, event) :
        self.send(text_data=json.dumps(event['event']))
        self.battle.delete()

    def start (self,event) :

        self.send(text_data=event['event'])