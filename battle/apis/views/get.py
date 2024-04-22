from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from ...models import Battle


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

        if user not in battle.users.all() or battle.users.all().count() == 1: 
            return Response({
                'message' : "battle not found"
            },status=status.HTTP_404_NOT_FOUND)
        
        data = {
            'players' : battle.get_players(me=request.user),
            'text' : battle.text,
        }

        return Response(data,status=status.HTTP_200_OK)