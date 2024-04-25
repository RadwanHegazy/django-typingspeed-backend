from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from ...models import Battle
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
class get_battle(APIView) : 
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, battle_id,**kwargs) : 
        
        try : 
            battle = Battle.objects.get(id=battle_id)
        except Battle.DoesNotExist:
            return Response({
                'message' : "battle not found"
            },status=status.HTTP_404_NOT_FOUND)
        
        user = request.user

        if user not in battle.users.all(): 
            return Response({
                'message' : "battle not found"
            },status=status.HTTP_404_NOT_FOUND)
        
        if battle.users.count() == 2 :
            # create real-time msgsing 
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'battle_{battle_id}',{
                    'type' : 'start',
                    'event': json.dumps({
                        'start' : 1,
                        'friend' : {
                            'full_name' : request.user.full_name,
                            'picture' : request.user.picture.url,
                           }
                        }
                    )
                }
            )
            

        data = {
            'players' : battle.get_players(me=request.user),
            'text' : battle.text,
        }

        return Response(data,status=status.HTTP_200_OK)