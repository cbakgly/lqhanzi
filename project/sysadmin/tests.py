#!/usr/bin/python
import json
import pdb
import random
import os, binascii
from datetime import datetime

from django.test import TestCase
from sysadmin.models import User
from sysadmin.models import Operation
from django.test import Client


class OperationTestCase(TestCase):
    def setUp(self):
        self.url = "/sysadmin/operation/"
        # Create tmp user
        self.tmp_msg = binascii.b2a_hex(os.urandom(15))
        self.tmp_username = self.tmp_msg[:5]
        self.datetime = datetime.now()
        user = User.objects.create(username=self.tmp_username)
        user.set_password(self.tmp_username)
        user.save()

        # Create tmp message
        self.logtype = random.randint(1, 200)
        operation = Operation(user=user, logtype=self.logtype, logtime=self.datetime, message=self.tmp_msg)
        operation.save()

    def test_get_one_operation(self):
        payload = {"user__username": self.tmp_username, "logtype": self.logtype, "message__contains": self.tmp_msg[:10]}
        response = self.client.get(self.url, payload)
        data = json.loads(response.content)
        get_msg = data['results'][0].get('message')
        self.assertEqual(get_msg, self.tmp_msg)

    def test_post_operation(self):
        payload = {"user": 1, "logtime": datetime.now().isoformat(), "message": binascii.b2a_hex(os.urandom(15)), "logtype": 1}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 201) # 201 HTTP CREATED CODE

    def test_delete_one_record_operation(self):
        response = self.client.delete("/sysadmin/operation/1/")
        self.assertGreater(response.status_code, 200)
