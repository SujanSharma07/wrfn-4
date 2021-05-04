from rest_framework import serializers
from account.models import *
from main.models import *
from rest_framework import permissions


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        #fields = "__all__"
        fields = ['id','username','password','country','first_name','last_name','is_verified','is_otp_verified','is_admin','phone','membership']
        extra_kwargs = {'password':{'write_only':True,'min_length':10}}
#        exclude = ['password']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user    


class Personal_InfoSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

   # user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Personal_Info
        fields = "__all__"
        
    def create(self,validated_data,user):
        user = super().create(validated_data)
        user.user = user
        user.save()
        return user    

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = "__all__"
         

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = "__all__"

        extra_kwargs = {"area": {"required": False, "allow_null": True},
                        "experience": {"required": False, "allow_null": True},
                        "hard_skills": {"required": False, "allow_null": True},
                        "soft_skills" : {"required": False, "allow_null": True},
                        "interests": {"required": False, "allow_null": True}}

         
 
       
      