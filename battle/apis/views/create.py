from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from ...models import Battle


class create_battle(APIView) : 
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request,**kwargs) : 
        
        battle = Battle.objects.create()
        battle.users.add(request.user)
        battle.save()
        
        data = {
            'battle_id' : str(battle.id)
        }
        
        return Response(data,status=status.HTTP_200_OK)