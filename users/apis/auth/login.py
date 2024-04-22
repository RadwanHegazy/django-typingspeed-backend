from rest_framework.views import APIView
from ..serializers import LoginSerializer
from rest_framework import status
from rest_framework.response import Response

class login_view(APIView) :
    serializer_class = LoginSerializer

    def post(self,request,**kwargs) : 
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid() : 
            return Response(serializer.tokens,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        