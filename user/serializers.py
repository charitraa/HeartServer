from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with all required fields.
    """
    username = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    confirm_password = serializers.CharField(write_only=True, min_length=8, required=True)
    class Meta:
        model = User
        fields = ['username', 'full_name', 'password', 'confirm_password']


    def validate(self, attrs):
        # Ensure passwords match
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"message": "Passwords do not match."})
        # Validate password strength using Django’s built-in validators
        # validate_password(attrs['password'])

        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"message": "Username is already taken."})
        
        if len(attrs['full_name'].strip().split()) < 2:
            raise serializers.ValidationError({"message": "Full name must include at least first and last name."})
        
        if ' ' in attrs['username']:
            raise serializers.ValidationError({"message": "Username must not contain spaces."})
        
        if len(attrs['username']) < 3:
            raise serializers.ValidationError({"message": "Username must be at least 3 characters long."})
        if len(attrs['password']) < 8:
            raise serializers.ValidationError({"message": "Password must be at least 8 characters long."})
        if attrs['username'].lower() in attrs['password'].lower():
            raise serializers.ValidationError({"message": "Password is too similar to the username."})
        return attrs


    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            full_name=validated_data['full_name'],
            password=validated_data['password'],
            username=validated_data['username'],
        )
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'groups': {'write_only': True},
            'user_permissions': {'write_only': True},
        }


# class UserUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email', 'username']

#     def update(self, instance, validated_data):
#         # Prevent email duplication
#         if 'email' in validated_data:
#             new_email = validated_data['email']
#             if User.objects.filter(email=new_email).exclude(id=instance.id).exists():
#                 raise serializers.ValidationError({"email": "This email is already in use."})
        
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance
