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
        return self.on_get(request)


    def post(self, request):
        return self.on_post(request)


    def on_get(self, request):

        email = request.GET.get('email')
        username = request.GET.get('username')
        password = request.GET.get('password')
        token = None
        try:
            user = User.objects.all().get(username=username)
            if user is not None and user.check_password(password):

                if user.is_active:
                    jira_verify_obj = JIRA(server='https://mpulsemobile.atlassian.net', basic_auth=(username, password),
                                           max_retries=0, logging=False)
                    if not jira_verify_obj:
                        self.login_successful = False
                        user.delete()
                        self.reason = 'Your Password has expired. Update and Re-Register'
                    else:
                        token, created = Token.objects.get_or_create(user=user)
                        request.session['auth'] = token.key
                        self.login_successful = True
            else:
                    self.login_successful = False
                    self.reason = 'Incorrect Username or Password.'
        except Exception as e:
            self.login_successful = False
            self.reason = 'Your Password has expired. Update and Re-Register'

        response_data = {'successful':self.login_successful, 'reason': self.reason, 'token':token.key if token else None}
        return HttpResponse(json.dumps(response_data), status=201, content_type='application/json')


    def on_post(self, request):

        registration_error = 'None'
        body = request.data
        username = body.get('username')
        password = body.get('password')
        email_id = body.get('email-id')

        try:
            jira_verify_obj = JIRA(server='https://mpulsemobile.atlassian.net', basic_auth=(username, password), max_retries=0, logging=False)
            if not jira_verify_obj:
                self.is_registered = False
                registration_error = 'Invalid JIRA Credentials'
            else:
                user = User.objects.create_user(username, email_id, password)
                user.save()
        except JIRAError as e:
            self.is_registered = False
            registration_error = "Username and Password combination doesn't match any Active User."

        except Exception as e:
            self.is_registered = False
            registration_error = 'Duplicate Entry for Username %s'%username

        response_data = {'registered': self.is_registered, 'error': registration_error}
        return HttpResponse(json.dumps(response_data), status=201, content_type='application/json')

