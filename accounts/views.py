from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.messages.context_processors import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, redirect
from jira import JIRAError
from rest_framework import request
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from jira.client import JIRA
from rest_framework.authtoken.models import Token
# Create your views here.
import json


def login_form(request):
    return render_to_response('login.html',{})


class LoginAccount(APIView):

    login_successful = True
    is_registered = True
    error_in_registration = None
    reason = ''

    def get(self, request):
        pass

    def post(self, request):
        body = request.data
        username = body.get('username')
        password = body.get('password')
        token = None

        try:

            jira_verify_obj = JIRA(server='https://mpulsemobile.atlassian.net', basic_auth=(username, password),
                                   max_retries=0, logging=False)
            if not jira_verify_obj:
                self.login_successful = False
                self.reason = 'Invalid username or password'
            else:
                user = User.objects.filter(username=username).first()
                if user is not None and not user.check_gipassword(password):
                    user.set_password(password)
                else:
                    user = User.objects.create_user(username, password)
                user.save()
                token, created = Token.objects.get_or_create(user=user)

        except Exception as e:
            self.login_successful = False
            self.reason = 'Invalid username or password'

        response_data = {
            'successful': self.login_successful,
            'reason': self.reason,
            'token': token.key if token else None
        }

        return HttpResponse(json.dumps(response_data), status=201, content_type='application/json')


