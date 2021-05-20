from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
  Login,
  log_out,
)

app_name = 'account'

urlpatterns = [ 
  path('login', Login.as_view(), name='login'),   
  path('log_out', log_out, name='log_out'),  
]
