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
        # SetUp will execute everytime before each test case 
        print "<Test sysadmin apps...>"
        print "-----------------------------------\n"
        self.url = "/sysadmin/operation/"
        # Create tmp user
        self.tmp_msg = binascii.b2a_hex(os.urandom(15))
        self.tmp_username = self.tmp_msg[:5]
        user = User.objects.create(username=self.tmp_username)
        user.set_password(self.tmp_username)
        user.save()

        # Create tmp message
        self.logtype = random.randint(0, 5) # Because logtype in (0, 1, 2, 3, 4, 5) if more than 5 it can not get data by filter
        operation = Operation(user=user, logtype=self.logtype, message=self.tmp_msg)
        operation.save()


    def test_get_one_operation(self):
        payload = {"user__username": self.tmp_username, "logtype": self.logtype, "message__contains": self.tmp_msg[:10]}
        response = self.client.get(self.url, payload)
        data = json.loads(response.content)
        get_msg = data['results'][0]['message']
        print "test_get_one_operation: {0} {1}".format(response.status_code, response.content)
        #pdb.set_trace()
        self.assertEqual(get_msg, self.tmp_msg)


    def test_post_operation(self):
        payload = {"user": 1, "message": binascii.b2a_hex(os.urandom(15)), "logtype": 1}
        response = self.client.post(self.url, payload)
        print "test_post_operation: {0} {1}".format(response.status_code, response.content)
        self.assertEqual(response.status_code, 201) # 201 HTTP CREATED CODE


    def test_put_operation(self):
        test_id = Operation.objects.all()[0].id
        payload = {"user": 1, "message": binascii.b2a_hex(os.urandom(15)), "logtype": 1}
        payload = json.dumps(payload)
        url = "{0}{1}/".format(self.url, test_id)
        #print url
        response = self.client.put(url, payload, content_type='application/json')
        print "test_put_operation: {0} {1}".format(response.status_code, response.content)
        #pdb.set_trace()
        self.assertLess(response.status_code, 300) 

    def test_delete_one_record_operation(self):
        id = Operation.objects.all().values()[0]['id']
        response = self.client.delete("/sysadmin/operation/{0}/".format(id))
        print "test_delete_one_record_operation: {0} {1}".format(response.status_code, response.content)
        self.assertGreater(response.status_code, 200)


    def test_add_user(self, username="xianer", password="xianer"):
        payload = {"username": username, "password": password, "first_name": "shi", "last_name": "xianer",\
                    "email": "xianer@gmail.com", "is_active": 1, "gender": 1, "mb": "15899990045", \
                    "qq": "375944090", "address": "Lq" }
        
        response = self.client.post("/sysadmin/user/", payload)
        print "test_add_user: {0}, {1}".format(response.status_code, response.content)
        self.assertEqual(response.status_code, 201)
        return response


    def test_add_users(self):
        add_user_num = 2
        success_status_code_list = []
        for i in range(add_user_num):
            username = "test_user_{0}".format(i)
            password = "test_password_{0}".format(i)
            response = self.test_add_user(username, password)
            if response.status_code == 201: success_status_code_list.append(response.status_code)
        success_count = len(success_status_code_list)
        print "<Success added: {0} users>".format(success_count)
        self.assertEqual(success_count, add_user_num)


    def test_get_all_users(self):
        url = "/sysadmin/user/"
        response = self.client.get(url)
        print "test_get_all_users: {0}, {1}".format(response.status_code, response.content)
        self.assertEqual(response.status_code, 200)

"""
All functions must be start with 'test' if you want to test the case, or else it did not run
"""
