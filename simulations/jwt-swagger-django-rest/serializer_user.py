from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers


User = get_user_model()


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'password', 'email', 'is_staff')

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
# end of UserSerializer
