from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "profilepic", "moredesc",
                  "businessname", "slug", "country", "state", "address", "phone", "email", "meansofid", "idnumber", "idpic", "logo", "currency", "coins", "whatsapp", "facebook", "instagram", "username", "password", "gender", "updated", "created", "subscribed", "passwordresetcode", "passwordresetphone", "securityquestion", "securityanswer", "date", "trial_start", "trial_end"]
