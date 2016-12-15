#!/usr/bin/python
import json
import requests
import random
import os, binascii
from datetime import datetime

from django.test import TestCase
from sysadmin.models import User
from sysadmin.models import Operation


class OperationTestCase(TestCase):
    def setUp(self):
        self.url = "http://127.0.0.1:8000/sysadmin/operation/"
        # Create tmp user
        self.tmp_msg = binascii.b2a_hex(os.urandom(15))
        self.tmp_username = self.tmp_msg[:5]
        self.datetime = datetime.now()
        user = User.objects.create(username=self.tmp_username)
        user.set_password(self.tmp_username)
        user.save()

        # Create tmp message
        operation = Operation(user=user, logtype=random.randint(1, 200), logtime=self.datetime, message=self.tmp_msg)
        operation.save()

    def test_get_operations(self):

        payload = {"user__username": self.tmp_username}
        r = requests.get(self.url, params=payload)
        print r.url
        print r.json()
        #self.assertEqual(message, self.tmp_msg)
