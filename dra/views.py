import base64
import json
import time
import jwt
import logging
from django.http import HttpResponse
from django.conf import settings
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from dra.models import Account
from dra.util import PrivateKey
from dra.auth import get_account_repository_permissions

logger = logging.getLogger(__name__)

TOKEN_LIFETIME = 300


@csrf_exempt
def token(request):
    """ This view authenticates and issues tokens """

    if request.method != 'GET':
        return HttpResponse(status=404)

    auth = request.META.get('HTTP_AUTHORIZATION', None)
    if auth is None:
        return HttpResponse(status=403)

    meth, token = auth.split(' ', 1)
    if meth.lower() != 'basic':
        return HttpResponse(status=403)

    user, password = base64.b64decode(token.strip().encode()).decode().split(':')

    account = Account.objects.filter(username=user).first()
    if account is None or not account.check_password(password):
        return HttpResponse(status=403)

    Account.objects.filter(pk=account.pk).update(requests=F('requests') + 1)

    service = request.GET['service']
    now = int(time.time())

    resp = {
        'iss': settings.DRA_ISS,
        'sub': account.username,
        'aud': service,
        'exp': now + TOKEN_LIFETIME,
        'nbf': now,
        'iat': now,
        'jti': '1',
        'access': [],
    }

    for scope in request.GET.getlist('scope'):
        ss = scope.split(':')
        if len(ss) == 3:
            typ, repo, _ = ss
            if typ == 'repository':
                pull, push = get_account_repository_permissions(account=account, repository=repo)
                actions = []
                if pull:
                    actions.append('pull')
                if push:
                    actions.append('push')

                resp['access'].append({
                    'type': typ,
                    'name': repo,
                    'actions': actions,
                })

                logger.info("Account=%s Repo=%s: permissions granted: pull=%s push=%s",
                            account, repo, pull, push)

    response = HttpResponse()
    response['Content-type'] = 'application/json'

    key = PrivateKey(settings.RSA_KEY)

    response.write(json.dumps({
        'token': jwt.encode(
            resp,
            key.key,
            algorithm='RS512',
            headers={'kid': key.public_key_kid},
        ),
        'expires_in': TOKEN_LIFETIME,
    }))

    return response
