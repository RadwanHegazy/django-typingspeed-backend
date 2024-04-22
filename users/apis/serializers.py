from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from rest_framework.validators import ValidationError

class LoginSerializer (serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        try :
            self.user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError({
                'message' : "invalid email"
            },code=400)

        if not self.user.check_password(password) : 
            raise ValidationError({
                'message' : "invalid password"
            },code=400)
            
            

        return attrs
    


    @property
    def tokens (self):
        token = RefreshToken.for_user(self.user)
        return {
            'access' : str(token.access_token)
        }

class RegisterSerializer (serializers.ModelSerializer) :
    class Meta:
        model = User
        fields = ('id','full_name','email','password','picture')
    
    def save(self, **kwargs):
        self.user = User.objects.create_user(**self.validated_data)
        self.user.save()
        return self.user
    
    
    @property
    def tokens (self):
        token = RefreshToken.for_user(self.user)
        return {
            'access' : str(token.access_token)
        }