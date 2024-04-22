from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

class profile_view(APIView) :
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,**kwargs) : 
        user = request.user
        data = {
            'picture' : user.picture.url,
            'full_name' : user.full_name,
            'points' : user.points,
        }
        
        return Response(data,status=status.HTTP_200_OK)
        