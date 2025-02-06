from tortoise import fields
from tortoise.models import Model

class User(Model):
    banned = fields.BooleanField()
    disactivated = fields.BooleanField()

    id = fields.IntField(pk=True)  
    name = fields.CharField(max_length=25)
    lastname = fields.CharField(max_length=15)
    username = fields.CharField(max_length=25)
    date_of_birth = fields.DateField()  
    gender = fields.CharField(max_length=1)
    email = fields.CharField(max_length=30)
    password = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return self.name + self.lastname + str(self.id)
    
    class Meta:
        table = "User"
