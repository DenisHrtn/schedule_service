from rest_framework import serializers

from users.models.profile import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user', 'days_with_service']


class ProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=25)
    last_name = serializers.CharField(max_length=25)
    about_me = serializers.CharField(required=False)
    sex = serializers.CharField(required=False)
    photo = serializers.ImageField(required=False)
    city = serializers.CharField(max_length=45)
    country = serializers.CharField(max_length=45)
    use_service_for = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.about_me = validated_data.get('about_me', instance.about_me)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.city = validated_data.get('city', instance.city)
        instance.country = validated_data.get('country', instance.country)
        instance.use_service_for = validated_data.get('use_service_for', instance.use_service_for)
        instance.save()
        return instance