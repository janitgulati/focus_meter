from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets, response, permissions

from .serializers import UserSerializer

def index(request):
	template=loader.get_template('index2.html')
	return HttpResponse(template.render(request))

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk=None):
        if pk == 'i':
            return response.Response(UserSerializer(request.user,
                context={'request':request}).data)
        return super(UserViewSet, self).retrieve(request, pk)
