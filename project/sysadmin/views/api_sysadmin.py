from django.shortcuts import render
from rest_framework.views import APIView
from sysadmin.models import User
from sysadmin.models import Operation
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

class OperationView(APIView):
    def get(self, request):
        user = User.objects.get(username=request.user)
        username, begin_at, end_at, logtype = (self.request.query_params.get(key, None) for key in \
                ("username", "begin_at", "end_at"))

        #operation_list = Operation.objects.filter(user=user

        return Response({"message": "for test"})
