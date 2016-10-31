import socket
import json
import time
import jwt
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from dra.models import Account
from dra.util import PrivateKey
from dra.auth import get_account_repository_permissions

# Create your views here.

def token(request):
    """ This view authenticates and issues tokens """

    auth = request.META.get('HTTP_AUTHORIZATION', None)
    if auth is None:
        return HttpResponse(status=403)

    meth, token = auth.split(' ', 1)
    if meth.lower() != 'basic':
        return HttpResponse(status=403)

    user, password = token.strip().decode('base64').split(':')

    account = Account.objects.filter(username=user).first()
    if account is None or not account.check_password(password):
        return HttpResponse(status=403)

    service = request.GET['service']
    now = int(time.time())

    resp = {
            'iss': socket.getfqdn(),
            'sub': account.username,
            'aud': service,
            'exp': now + 60,
            'nbf': now,
            'iat': now,
            'jti': '1',
            }

    scope = request.GET.get('scope', None)
    if scope is not None:
        ss = scope.split(':')
        if len(ss) == 3:
            typ, repo, ops = ss
            if typ == 'repository':
                pull, push = get_account_repository_permissions(account=account, repository=repo)
                actions = []
                if pull:
                    actions.append('pull')
                if push:
                    actions.append('push')

                resp['access'] = [
                        {
                            'type': typ,
                            'name': repo,
                            'actions': actions
                        }
                        ]

    response = HttpResponse()
    response['Content-type'] = 'application/json'

    key = PrivateKey(settings.RSA_KEY)

    response.write(json.dumps({
        'token': jwt.encode(
            resp,
            key.key,
            algorithm='RS512',
            headers={'kid':key.public_key_kid},
            )
        }))

    return response
