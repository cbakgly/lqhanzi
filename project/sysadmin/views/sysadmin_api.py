from django.shortcuts import render
from rest_framework.views import APIView
from sysadmin.models import User
from sysadmin.models import Operation
from rest_framework.response import Response

class OperationView(APIView):
    def get(self, request):
        return Response({"message": "for test"})
