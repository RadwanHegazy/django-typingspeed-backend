from django.db import models
from uuid import uuid4
from users.models import User
from essential_generators import DocumentGenerator
from django.dispatch import receiver
from django.db.models.signals import post_save
import threading

class Battle(models.Model) :
    id = models.UUIDField(primary_key=True,editable=False,default=uuid4)
    users = models.ManyToManyField(User,related_name='users_in_battle')
    winner = models.ForeignKey(User,related_name='battle_winner',on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(null=True,blank=True)
    
    def __str__(self) -> str:
        return str(self.id)

    
    def get_players(self,me) : 
        data = {
            'me' : None,
            'friend' : None,
        }
        for user in self.users.all() : 
            if user == me :
                data['me'] = self.serialize_user(user)
            else:
                data['friend'] = self.serialize_user(user)
                
        return data
    
    @staticmethod
    def serialize_user (user) : 
        return {
            'full_name' : user.full_name,
            'picture' : user.picture.url,
            'id' : user.id,
        }
    


@receiver(post_save,sender=Battle)
def generate_battle_text (created,instance:Battle,**kwargs) : 
    if created :
        doc = DocumentGenerator()
        instance.text = doc.paragraph(min_sentences=5,max_sentences=15)
        instance.save()