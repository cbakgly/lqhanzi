#!/usr/bin/python
import json
import pdb
import random
import os, binascii
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
        user = User.objects.create(username=self.tmp_username)
        user.set_password(self.tmp_username)
        user.save()

        # Create tmp message
        self.logtype = random.randint(1, 200)
        operation = Operation(user=user, logtype=self.logtype, message=self.tmp_msg)
        operation.save()

    def test_get_one_operation(self):
        payload = {"user__username": self.tmp_username, "logtype": self.logtype, "message__contains": self.tmp_msg[:10]}
        response = self.client.get(self.url, payload)
        data = json.loads(response.content)
        get_msg = data['results'][0].get('message')
        self.assertEqual(get_msg, self.tmp_msg)

    def test_post_operation(self):
        payload = {"user": 1, "message": binascii.b2a_hex(os.urandom(15)), "logtype": 1}
        response = self.client.post(self.url, payload)
        #print response.content
        self.assertEqual(response.status_code, 201) # 201 HTTP CREATED CODE

    def test_put_operation(self):
        test_id = Operation.objects.all()[0].id
        payload = {"user": 1, "message": binascii.b2a_hex(os.urandom(15)), "logtype": 1}
        payload = json.dumps(payload)
        url = "{0}{1}/".format(self.url, test_id)
        #print url
        response = self.client.put(url, payload, content_type='application/json')
        #print response.content
        #pdb.set_trace()
        self.assertLess(response.status_code, 300) # 201 HTTP CREATED CODE

    def test_delete_one_record_operation(self):
        response = self.client.delete("/sysadmin/operation/1/")
        self.assertGreater(response.status_code, 200)
