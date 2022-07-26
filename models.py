from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(Model):

    bank_id = fields.IntField(pk=True)
    #: This is a username
    user_id = fields.IntField(max_length=50, unique=True)
    acc_no = fields.CharField(max_length=50, null=False)
    ifcr_no = fields.CharField(max_length=50, null=False)
    micr_no = fields.CharField(max_length=50, null=False)
    swift = fields.CharField(max_length=50, null=False)


User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)