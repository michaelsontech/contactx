from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from django.db import transaction
from django.contrib.auth import get_user_model

from .utils import retrieve_user_data

User = get_user_model()


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):        
      data = JSONParser().parse(request)

      if data:
        password = data['password']
        email = data['email']

      if not email:
        res = {
          'status': 'error',
          'message': 'Enter a valid  email address'
        }
        return Response( res, status=status.HTTP_400_BAD_REQUEST)
      elif not password:
        res = {
          'status': 'error',
          'message': 'Enter a valid password'
        }
        return Response( res, status=status.HTTP_400_BAD_REQUEST)

      # try:
      #   # Validate.
      #   valid = validate_email(email)

      #   # Update with the normalized form.
      #   email = valid.email
      # except EmailNotValidError as e:
      #   # email is not valid, exception message is human-readable
      #   print(str(e))  

      #   res['message'] = 'invalid email'
      #   res['status'] = 'error'
      #   return Response( res, status=status.HTTP_400_BAD_REQUEST) 
   
      
      user = authenticate(request, email=email, password=password)

      if user is not None:
        token = Token.objects.get(user=user).key                
        user_data = retrieve_user_data(user.id)
                
        res = {
          'token': token,
          'user_data': user_data,
          'status': 'success',
          'message': 'Login successful'
        }
        return Response(res)
      else:
        res = {
          'status': 'error',
          'message': 'Incorrect email or password.'
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def log_out(request):

  if request.method == 'GET':

    user_token = Token.objects.get(key=request.auth.key)
    user_id = Token.objects.get(key=request.auth.key).user_id
    
    res = {}

    if user_token: 
      user_token.delete()
    else:
      return Response(status=status.HTTP_401_UNAUTHORIZED)
          
    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      res['message'] = 'invalid request.'
      res['status'] = 'error'
      return Response( res, status=status.HTTP_400_BAD_REQUEST)     
    
    Token.objects.create(user=user)


    res = {
      'status': 'success',
      'message': 'Log out successful.'
    }

    return Response(res, status=status.HTTP_200_OK)


