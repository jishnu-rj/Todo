from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ToDo(models.Model):
    title=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True)
    user_object=models.ForeignKey(User,on_delete=models.CASCADE)
    options=(
        ("pending","pending"),
        ("completed","completed"),
        
    )
    status=models.CharField(max_length=200,choices=options,default="pending")


    def _str_(self):
        return self.title