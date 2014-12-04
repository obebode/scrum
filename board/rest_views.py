from rest_framework import viewsets
from .models import Sprint, Task
from .serializers import SprintSerializer, TaskSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import authentication, permissions, viewsets, filters

User = get_user_model()


class DefaultsMixin(object):
    """
    Default settings for view authentication, permissions,
    filtering and pagination.
    """

    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


# Note - I intentionally did not set the defaultmixin to the viewsets
class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint of creating & listing tasks
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description')
    ordering_fields = ('name', 'order', 'started', 'due', 'completed', )


class SprintViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing & creating sprints
    """
    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions for users.
    """
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = (User.USERNAME_FIELD, )
    ordering_fields = (User.USERNAME_FIELD, )





