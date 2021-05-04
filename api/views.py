#API

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser 
from .serializers import *
from account.models import *
from main.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import permissions
from .custompermissions import *
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly


# User Model
@api_view(['GET','PUT','DELETE'])
def user_detail(request,pk):
    try:
        user = User.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user == user:

            data = JSONParser().parse(request)
            serializer = UserSerializer(instance=user, data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response({"message":"You are not allowed to Update this user "})    

    elif request.method == 'DELETE':
        if request.user.is_admin:
            user.delete()
            return HttpResponse(status=204)
        else:
            return Response({"message":"You are not allowed to delete a user"})    



@api_view(['GET','POST'])
@permission_classes([permissions.AllowAny])

def user_list(request):
    """
    List all code users, or create a new User.
    """
    if request.method == 'GET':
        snippets = User.objects.all()
        serializer = UserSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)        




# Personal Info
@api_view(['GET','PUT','DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,])
def p_detail(request,pk):
    try:
        user = User.objects.get(pk=pk)
        personal = Personal_Info.objects.get(user=user)
    except personal.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = Personal_InfoSerializer(personal)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if user == request.user:
            data = JSONParser().parse(request)
            serializer = Personal_InfoSerializer(instance=personal, data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response({'message':"You are not authorized to edit this"})

    elif request.method == 'DELETE':
        if request.user.is_admin:
            personal.delete()
            return HttpResponse(status=204)
        return Response({'message':"You are not authorized to do this operation"})
    

@api_view(['GET','POST'])
def p_list(request):
    """
    List all code users, or create a new User.
    """
    if request.method == 'GET':
        snippets = Personal_Info.objects.all()
        serializer = Personal_InfoSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Personal_InfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)        






# Documents
@api_view(['GET','PUT','DELETE'])
def d_detail(request,pk):
    try:
        user = User.objects.get(pk=pk)
        personal = Documents.objects.get(user=user)
    except personal.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DocumentSerializer(personal)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if user == request.user:
            from main.forms import Document_Form
            document = Document_Form(request.POST,request.FILES,instance=personal)
            if document.is_valid():
                document.user = request.user
                document.save()
                return Response({"message":"Updated Successfully"}, status=201)
            return Response({'message':"Invalid request"}, status=400)   

        return Response({'message':"You are not authorized to do this operation"})
    

    elif request.method == 'DELETE':
        if request.user.is_admin:
            personal.delete()
            return HttpResponse(status=204)
        return Response({'message':"You are not authorized to do this operation"})


@api_view(['GET','POST'])
def d_list(request):
    """
    List all code users, or create a new User.
    """
    if request.method == 'GET':
        snippets = Documents.objects.all()
        serializer = DocumentSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        from main.forms import Document_Form
        document = Document_Form(request.POST,request.FILES)
        if document.is_valid():
            document.user = request.user
            document.save()
            return Response({"message":"Uploaded Successfully"}, status=201)
        return Response({'message':"Invalid request"}, status=400)    







# Skills
@api_view(['GET','PUT','DELETE'])
def s_detail(request,pk):

    try:
        user = User.objects.get(pk=pk)
        personal = Skills.objects.get(user=user)
    except personal.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SkillSerializer(personal)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if user == request.user:

            data = JSONParser().parse(request)
            serializer = SkillSerializer(instance=personal, data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response({'message':"You are not authorized to do this operation"})


    elif request.method == 'DELETE':
        if request.user.is_admin:
            personal.delete()
            return HttpResponse(status=204)
        return Response({'message':"You are not authorized to do this operation"})


@api_view(['GET','POST'])
def s_list(request):
    """
    List all code users, or create a new User.
    """
    if request.method == 'GET':
        snippets = Skills.objects.all()
        serializer = SkillSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SkillSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)    