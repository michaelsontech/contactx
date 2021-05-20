from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user(headers):    
    try:
        auth_list = headers[b'sec-websocket-protocol'].decode()        
        token_key = ''
        for i in range(14, len(auth_list)):
            token_key += auth_list[i]

        # print(auth_list) 
        # print(token_key)
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        # print('anonymous')
        return AnonymousUser()


class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
    """
    Yeah, this is black magic:
    https://github.com/django/channels/issues/1399
    """
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):        
        headers = dict(self.scope['headers'])
        if b'sec-websocket-protocol' in headers:
            self.scope['user'] = await get_user(headers)        
        # inner = await self.inner(self.scope, receive, send)
            return await self.inner(self.scope, receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))