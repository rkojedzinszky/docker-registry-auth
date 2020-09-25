import base64
import json
import socket
import logging
import sys
from django.test import TestCase
from dra import models
from django.test import Client
from django.conf import settings
import subprocess, os
from jwt.utils import base64url_decode

SERVICE = 'test.service'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'
RO_USERNAME = 'ro'
RO_PASSWORD = 'ro'

class AuthTest(TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.check_call(['openssl', 'genrsa', '-out', settings.RSA_KEY, '2048'])

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

        ro_group = models.Group.objects.create(name='ro_group')
        admin_group = models.Group.objects.create(name='admin')
        u1 = models.Account(username=ADMIN_USERNAME)
        u1.set_password(ADMIN_PASSWORD)
        u1.save()
        u1.groups.set([ro_group, admin_group])

        rouser = models.Account(username=RO_USERNAME)
        rouser.set_password(RO_PASSWORD)
        rouser.save()

        pub_repo = models.Repository.objects.create(name='public', public=True)
        priv_repo = models.Repository.objects.create(name='private')

        org_repo = models.Repository.objects.create(name='org')
        models.Repository.objects.create(name='org/public', public=True)
        org_pub_priv_repo = models.Repository.objects.create(name='org/public/private')

        models.RepositoryPermissions.objects.create(repository=pub_repo, group=ro_group, write=False)
        models.RepositoryPermissions.objects.create(repository=pub_repo, group=admin_group, write=True)
        models.RepositoryPermissions.objects.create(repository=priv_repo, group=admin_group, write=True)

        models.RepositoryPermissions.objects.create(repository=org_repo, group=admin_group, write=True)

        models.RepositoryPermissions.objects.create(repository=org_pub_priv_repo, group=ro_group, write=False)

    def request(self, service=SERVICE, scope='registry:*', username=None, password=None):
        c = Client()
        extra = {}
        if username and password:
            extra['HTTP_AUTHORIZATION'] = 'Basic ' + base64.b64encode('{}:{}'.format(username, password).encode()).decode()

        return c.get('/token/', {'service': service, 'scope': scope}, **extra)

    def request_repository(self, repository, **kwargs):
        response = self.request(scope='repository:{}:pull,push'.format(repository), **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        response = json.loads(response.content)
        header, payload, signature = response['token'].split('.')

        payload = base64url_decode(str(payload)).decode('utf-8')
        return json.loads(payload)

    def test_noauth(self):
        self.assertEqual(self.request().status_code, 403)

    def test_badauth(self):
        self.assertEqual(self.request(username=ADMIN_USERNAME, password='{}a'.format(ADMIN_PASSWORD)).status_code, 403)

    def test_auth(self):
        response = self.request(username=ADMIN_USERNAME, password=ADMIN_PASSWORD)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_roauth(self):
        response = self.request(username=RO_USERNAME, password=RO_PASSWORD)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def _assert_payload(self, payload, sub=ADMIN_USERNAME):
        self.assertIsInstance(payload, dict)
        self.assertEqual(payload['aud'], SERVICE)
        self.assertEqual(payload['sub'], sub)
        self.assertEqual(payload['iss'], socket.getfqdn())

        if 'access' in payload:
            access = payload['access']
            self.assertIsInstance(access, list)
            self.assertEqual(len(access), 1)
            access = access[0]
            self.assertIsInstance(access, dict)

    def _assert_payload_repo(self, payload, repository, **kwargs):
        self._assert_payload(payload, **kwargs)
        access = payload['access'][0]
        self.assertEqual(access['type'], 'repository')
        self.assertEqual(access['name'], repository)
        return access['actions']

    def _repo_actions(self, username, password, repository):
        payload = self.request_repository(username=username, password=password, repository=repository)
        return self._assert_payload_repo(payload=payload, repository=repository, sub=username)

    def test_admin_repo_access(self):
        actions = self._repo_actions(username=ADMIN_USERNAME, password=ADMIN_PASSWORD, repository='public')

        self.assertIn('pull', actions)
        self.assertIn('push', actions)

    def test_admin_norepo_access(self):
        actions = self._repo_actions(username=ADMIN_USERNAME, password=ADMIN_PASSWORD, repository='nonexistent')

        self.assertNotIn('pull', actions)
        self.assertNotIn('push', actions)

    def test_ro_repo_access(self):
        actions = self._repo_actions(username=RO_USERNAME, password=RO_PASSWORD, repository='public')

        self.assertIn('pull', actions)
        self.assertNotIn('push', actions)

    def test_ro_repo_no_access(self):
        actions = self._repo_actions(username=RO_USERNAME, password=RO_PASSWORD, repository='private')

        self.assertNotIn('pull', actions)
        self.assertNotIn('push', actions)

    def test_recursive_ro_no_access(self):
        actions = self._repo_actions(username=RO_USERNAME, password=RO_PASSWORD, repository='private/repo1')

        self.assertNotIn('pull', actions)
        self.assertNotIn('push', actions)

        actions = self._repo_actions(username=RO_USERNAME, password=RO_PASSWORD, repository='private/repo2/sub')

        self.assertNotIn('pull', actions)
        self.assertNotIn('push', actions)

    def test_recursive_ro_access(self):
        actions = self._repo_actions(username=RO_USERNAME, password=RO_PASSWORD, repository='public/repo1')

        self.assertIn('pull', actions)
        self.assertNotIn('push', actions)

        actions = self._repo_actions(username=RO_USERNAME, password=RO_PASSWORD, repository='public/repo2/sub')

        self.assertIn('pull', actions)
        self.assertNotIn('push', actions)

    def test_org_public(self):
        actions = self._repo_actions(username=RO_USERNAME, password=RO_PASSWORD, repository='org/public/private')

        self.assertNotIn('pull', actions)
        self.assertNotIn('push', actions)

    def test_admin_priv_no_access(self):
        actions = self._repo_actions(username=ADMIN_USERNAME, password=ADMIN_PASSWORD, repository='org/public/private')

        self.assertIn('pull', actions)
        self.assertNotIn('push', actions)
