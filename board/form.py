import django_filters
from .models import Task
from board.serializers import TaskSerializer, UserSerializer, SprintSerializer
from rest_framework import viewsets, filters


# Specifying a FilterSet to be used by the views
# This is useful for advanced filtering requirements

# NullFilter will return all tasks not assigned to sprint
class TaskFilter(django_filters.FilterSet):
    backlog = NullFilter(name='sprint')

    class Meta:
        model = Task
        fields = ('sprint', 'status', 'assigned', )


class NullFilter(django_filters.FilterSet):
    """Filter on a field set as null or not."""
    def filter(self, qs, value):
        if value is not None:
            return qs.filter(**{'%s__isnull' % self.name: value})
        return qs


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint of creating & listing tasks
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description')
    ordering_fields = ('name', 'order', 'started', 'due', 'completed', )
