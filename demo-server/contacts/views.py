from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from .models import Contact
from .serializer import ContactSerializer

User = get_user_model()

class ContactView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):   
    """ Creates a new contact"""

    data = JSONParser().parse(request)    
    user_id = Token.objects.get(key=request.auth.key).user_id
    
    res = {}

    if data:
      full_name = data['full_name']
      phone_number = data['phone_number']
    
    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      res['message'] = 'invalid request.'
      res['status'] = 'error'
      return Response(res, status=status.HTTP_400_BAD_REQUEST)    

    Contact.objects.create(
      full_name=full_name,
      phone_number=phone_number,
      user=user,
    ) 
    contacts = Contact.objects.filter(user=user)
    serialized_contacts = ContactSerializer(contacts, many=True)

    res = {
      'message': 'Contact created successfully',
      'status': 'success',
      'contacts': serialized_contacts.data,
    }

    return Response(res, status=status.HTTP_201_CREATED)   

  def get(self, request):
    """ Fetches all contact"""

    user_id = Token.objects.get(key=request.auth.key).user_id    
    res = {}

    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      res['message'] = 'invalid request.'
      res['status'] = 'error'
      return Response(res, status=status.HTTP_400_BAD_REQUEST)    

    contacts = Contact.objects.filter(user=user)
    serialized_contacts = ContactSerializer(contacts, many=True)
    
    res = {
      'message': 'Contacts retrieved successfully',
      'status': 'success',
      'contacts': serialized_contacts.data,
    }

    return Response(res, status=status.HTTP_200_OK)   