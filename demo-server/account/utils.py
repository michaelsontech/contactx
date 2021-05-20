from django.contrib.auth import get_user_model
from .serializers import AccountSerializer

User = get_user_model()

def retrieve_user_data(user_id):
  """ Retrieves user's data after login or sign up """

  try: 
    user = User.objects.get(id=user_id)
  except User.DoesNotExist:
    res = {
      'status': 'error',
      'message': 'Invalid user id'
    }
    return res
  

  user_serialized = AccountSerializer(user)

  res = {
    'user_details': user_serialized.data,
  }
  
  return res