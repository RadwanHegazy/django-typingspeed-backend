from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from ...models import User

class profile_view(APIView) :
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,**kwargs) : 
        user:User = request.user
        data = {
            'picture' : user.picture.url,
            'full_name' : user.full_name,
            'points' : user.points,
            'leaders' : User.get_leaders()
        }
        
        return Response(data,status=status.HTTP_200_OK)
        