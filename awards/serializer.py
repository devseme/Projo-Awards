from rest_framework import serializers
from .models import Profile,Project

class MerchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user','profile_photo', 'bio', 'contact')