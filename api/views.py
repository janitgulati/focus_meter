from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets, response, permissions
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer

import ast
import json

from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from xml2json import xml2json
from rest_framework.permissions import IsAuthenticated

from jira.client import JIRA, JIRAError
from confluence import Api
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk=None):
        if pk == 'i':
            return response.Response(UserSerializer(request.user,
                context={'request':request}).data)
        return super(UserViewSet, self).retrieve(request, pk)


class CreateUserView(CreateAPIView):
    model = UserSerializer
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer


jira_obj = None
boards = None
issues_list = []


class SprintDetails(APIView):

    server = "https://mpulsemobile.atlassian.net"

    def get(self, request):
        if request.GET.get('sprint_id'):
            return self.get_current_sprint_information(request)
        else:
            return self.get_sprints_information(request)

    def get_sprints_information(self, request):
        global jira_obj
        global boards
        global issues_list
        status = 201
        sprint_info_dict = {}
        user = request.GET.get('username')
        password = request.GET.get('password')
        session = request.GET.get('session')

        sprints = None
        try:
            if 'true' in session and jira_obj == None:
                jira_obj = JIRA(server=self.server, basic_auth=(user, password))
                boards = jira_obj.boards()

            for board in boards:
                if 'mPulse' in board.name:
                    sprint_info_dict['board'] = board.name
                    sprints = jira_obj.sprints(board.id, state='ACTIVE')

            active_sprints_obj = filter(lambda sprint: sprint.state == 'ACTIVE', sprints)

            if active_sprints_obj:
                for active_sprint in active_sprints_obj:
                    sprint_info_dict['active_sprint'] = active_sprint.name
                    sprint_info_dict['active_sprint_id'] = active_sprint.id
                    # print(active_sprint.startDate)

            issues_list = jira_obj.search_issues('sprint=%s'%sprint_info_dict['active_sprint_id'])
            sprint_info_dict['issues_in_active_sprint'] = len(issues_list)
            future_sprints_obj = filter(lambda sprint: sprint.state == 'FUTURE', sprints)

            if future_sprints_obj:
                future_sprints = []
                for future_sprint in future_sprints_obj:
                    future_sprints.append({'name': future_sprint.name, 'id':future_sprint.id})
                sprint_info_dict['future_sprints'] = future_sprints

            sprint_info_dict['error'] = ''


        except JIRAError as e:
            status = 400
            sprint_info_dict['error'] = 'Error in Retrieving Information'


        return HttpResponse(json.dumps(sprint_info_dict), status=status, content_type='application/json')

    def get_current_sprint_information(self, request):
        ''' Also to add try except block here '''
        global jira_obj
        global issues_list
        issues_list = []
        sprint_info = {}
        sprint_name = request.GET.get('sprint_name')
        sprint_id = request.GET.get('sprint_id')
        session = request.GET.get('session')

        if 'true' in session and jira_obj:
            issues_list = jira_obj.search_issues('sprint=%s'%sprint_id)
            sprint_info['total_issues'] = len(issues_list)
            sprint_info['error']=''
        else:
            sprint_info['error']='Not Logged In'

        return HttpResponse(json.dumps(sprint_info), status=201, content_type='application/json')


class IssueDetails(APIView):

    def get(self, request):
        return self.get_all_issues_for_status(request)

    def get_all_issues_for_status(self, request):
        global jira_obj
        global issues_list

        print(issues_list)
        filter = request.GET.get('issue_filter_state')
        session = request.GET.get('session')

        issues_state = []
        issues_dict = {}
        if not session or not jira_obj:
            issues_dict['error'] = 'Not Logged In'

        else:
            # issues_dict['error'] = ''
            for issue in issues_list:
                issues_state.append(issue.fields.status.name)
                if filter in issue.fields.status.name:
                    issues_dict[issue.key] = {}
                    issues_dict[issue.key]['key'] = issue.key if issue.key else ''
                    issues_dict[issue.key]['desc'] = issue.fields.summary if issue.fields.summary else ''
                    issues_dict[issue.key]['assignee'] = issue.fields.assignee.displayName if issue.fields.assignee else ''
                    issues_dict[issue.key]['status'] = issue.fields.status.name  if issue.fields.status.name else ''
                    # issues_dict[issue.key]['environment'] = '' if not issue.fields.environment else issue.fields.environment
                    issues_dict[issue.key]['priority'] = issue.fields.priority.name if issue.fields.priority.name else ''

        issues_dict['distinct_states'] = list(set(issues_state))
        return HttpResponse(json.dumps(issues_dict), status=201, content_type='application/json')


class Sprints(APIView):
    permission_classes = (IsAuthenticated,)
    server = "https://mpulsemobile.atlassian.net"

    def get(self, request):
        if request.GET.get('sprint_id'):
            return self.get_selected_sprint_information(request)
        else:
            return self.get_sprints_information(request)

    def get_sprints_information(self, request):
        """

        Args:
            request:

        Returns: {
            board: board_name,
            sprints: [
                        {
                            "sprint_id": 1,
                            "sprint_name": "janit"
                        },
                        {
                            "sprint_id": 1,
                            "sprint_name": "janit"
                        }
                ],
            active_sprint_name: ,
            active_sprint_id: ,
            active_sprint_issue_count: ,
            future_sprints: [
                        {
                            "sprint_id": 1,
                            "sprint_name": "janit"
                        },
                        {
                            "sprint_id": 1,
                            "sprint_name": "janit"
                        }
                ]

        }
        """

        status = 201
        sprint_info_dict = {}
        user = "janit.gulati@mpulsemobile.com"
        password = "appworks@99"

        sprints = None
        try:

            jira_obj = JIRA(server=self.server, basic_auth=(user, password))
            boards = jira_obj.boards()

            for board in boards:
                if 'mPulse' in board.name:
                    sprint_info_dict['board'] = board.name
                    sprints = jira_obj.sprints(board.id)

            if sprints:
                sprint_info_dict['sprints'] = []
                for sprint in sprints:
                    # sprint_info_dict['sprints'].append({
                    #     "sprint_name": sprint.name,
                    #     "sprint_id": sprint.id
                    # })

                    sprint_info_dict['sprints'].append(
                        sprint.name + "#-#" + str(sprint.id)
                    )

            active_sprints_obj = filter(lambda sprint: sprint.state == 'ACTIVE', sprints)

            if active_sprints_obj:
                for active_sprint in active_sprints_obj:
                    sprint_info_dict['active_sprint_name'] = active_sprint.name
                    sprint_info_dict['active_sprint_id'] = active_sprint.id

            issues_list = jira_obj.search_issues('sprint=%s'%sprint_info_dict['active_sprint_id'])

            issues = []
            for issue in issues_list:
                # issues.append({
                #  'title': issue.raw['key'],
                # 'assignee': issue.raw['fields']['assignee']['emailAddress'],
                # 'type': issue.raw['fields']['issuetype']['name']
                #  })

                issues.append(
                    str(issue.raw['key']) + "#-#" + str(issue.raw['fields']['assignee']['emailAddress']) + "#-#" +
                    str(issue.raw['fields']['issuetype']['name'])
                )

            sprint_info_dict['active_sprint_issues'] = issues

            sprint_info_dict['active_sprint_issue_count'] = len(issues_list)
            future_sprints_obj = filter(lambda sprint: sprint.state == 'FUTURE', sprints)

            if future_sprints_obj:
                future_sprints = []
                for future_sprint in future_sprints_obj:
                    future_sprints.append({'sprint_name': future_sprint.name, 'sprint_id':future_sprint.id})
                sprint_info_dict['future_sprints'] = future_sprints

            sprint_info_dict['error'] = ''

        except JIRAError as e:
            status = 400
            sprint_info_dict['error'] = 'Error in Retrieving Information'

        return HttpResponse(json.dumps(sprint_info_dict), status=status, content_type='application/json')

    def get_selected_sprint_information(self, request):
        """

        Args:
            request:

        Returns: {
            board: board_name,
            sprints: [
                        {
                            "sprint_id": 1,
                            "sprint_name": "janit"
                        },
                        {
                            "sprint_id": 1,
                            "sprint_name": "janit"
                        }
                ],
            active_sprint_name: ,
            active_sprint_id: ,
            active_sprint_issue_count: ,
            future_sprints: [
                        {
                            "sprint_id": 1,
                            "sprint_name": "janit"
                        },
                        {
                            "sprint_id": 1,
                            "sprint_name": "janit"
                        }
                ]

        }
        """

        status = 201
        sprint_info_dict = {}
        user = "janit.gulati@mpulsemobile.com"
        password = "appworks@99"

        sprints = None
        sprint_id = request.GET.get('sprint_id')
        try:

            jira_obj = JIRA(server=self.server, basic_auth=(user, password))
            boards = jira_obj.boards()

            for board in boards:
                if 'mPulse' in board.name:
                    sprint_info_dict['board'] = board.name
                    sprints = jira_obj.sprints(board.id)

            selected_sprints_obj = filter(lambda sprint: sprint.id == int(sprint_id), sprints)

            if selected_sprints_obj:
                for selected_sprint in selected_sprints_obj:
                    sprint_info_dict['active_sprint_name'] = selected_sprint.name
                    sprint_info_dict['active_sprint_id'] = selected_sprint.id

            issues_list = jira_obj.search_issues('sprint=%s' % sprint_info_dict['active_sprint_id'])

            issues = []
            for issue in issues_list:
                # issues.append({
                #  'title': issue.raw['key'],
                # 'assignee': issue.raw['fields']['assignee']['emailAddress'],
                # 'type': issue.raw['fields']['issuetype']['name']
                #  })

                issues.append(
                        str(issue.raw['key']) + "#-#" + str(
                                issue.raw['fields']['assignee']['emailAddress']) + "#-#" +
                        str(issue.raw['fields']['issuetype']['name'])
                )

            sprint_info_dict['active_sprint_issues'] = issues

            sprint_info_dict['active_sprint_issue_count'] = len(issues_list)
            future_sprints_obj = filter(lambda sprint: sprint.state == 'FUTURE', sprints)

            if future_sprints_obj:
                future_sprints = []
                for future_sprint in future_sprints_obj:
                    future_sprints.append({'sprint_name': future_sprint.name, 'sprint_id': future_sprint.id})
                sprint_info_dict['future_sprints'] = future_sprints

            sprint_info_dict['error'] = ''

        except JIRAError as e:
            status = 400
            sprint_info_dict['error'] = 'Error in Retrieving Information'

        return HttpResponse(json.dumps(sprint_info_dict), status=status, content_type='application/json')
