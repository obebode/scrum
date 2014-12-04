from rest_framework import serializers
from .models import Sprint, Task
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from django.utils.translation import ugettext_lazy as _
from datetime import date


User = get_user_model()


class SprintSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField('get_links')

    class Meta:
            model = Sprint
            fields = ('id', 'name', 'description', 'end', 'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('sprint-detail',
                            kwargs={'pk': obj.pk}, request=request),
        }

    # Validation to allow the API not to create sprint that
    # have already happened or finished
    # This is a field level validation
    def validate_end(self, attrs, source):
        end_date = attrs[source]
        new = not self.object
        changed = self.object and self.object.end != end_date
        if (new or changed) and (end_date < date.today()):
            raise serializers.ValidationError("End date cannot be in the past.")
        return attrs


class TaskSerializer(serializers.ModelSerializer):
    assigned = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, required=False)
    status_display = serializers.SerializerMethodField('get_status_display')
    links = serializers.SerializerMethodField('get_links')

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'sprint', 'status', 'order',
                  'assigned', 'started', 'due', 'completed', 'links')

        def get_status_display(self, obj):
            return obj.get_status_display()

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('task-detail',
                            kwargs={'pk': obj.pk}, request=request),
            'sprint': None,
            'assigned': None
        }
        if obj.sprint_id:
            links['sprint'] = reverse('sprint-detail',
                                      kwargs={'pk': obj.sprint_id}, request=request)

        if obj.assigned:
                links['assigned'] = reverse('user-detail',
                                            kwargs={User.USERNAME_FIELD: obj.assigned}, request=request)
        return links

    # This is field level validation of the sprint field
    # Ensures that the sorint is not changed after task is completed
    #Tasks are not assigned to already completed sprints
    def validate_sprint(self, attrs, source):
        sprint = attrs[source]
        if self.object and self.object.pk:
            if sprint != self.object.sprint:
                if sprint.objects.status == Task.STATUS_DONE:
                    raise serializers.ValidationError("Cannot change the sprint of a completed task.")
                if sprint and sprint.end < date.today():
                    raise serializers.ValidationError("Cannot assign tasks to past sprints.")

        else:
            if sprint and sprint.end < date.today():
                raise serializers.ValidationError("Cannot add tasks to past sprints.")
        return attrs

    # This is the field level validation
    # Ensures that the combination of fields validates properly for the task
    def validate(self, attrs):
        status = int(attrs.get('status'))
        sprint = attrs.get('sprint')
        started = attrs.get('started')
        completed = attrs.get('completed')
        if not sprint and status != Task.STATUS_TODO:
            raise serializers.ValidationError("Backlog tasks must have Not Started status.")
        if started and status == Task.STATUS_TODO:
            raise serializers.ValidationError("Started date cannot be set for not started tasks.")
        if completed and status != Task.STATUS_DONE:
            raise serializers.ValidationError("Completed date cannot be set for uncompleted tasks.")
        return attrs



class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    links = serializers.SerializerMethodField('get_links')

    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active', 'links')

    def get_links(self, obj):
        request = self.context['request']
        username = obj.get_username()
        return {
            'self': reverse('user-detail',
                kwargs={User.USERNAME_FIELD: username}, request=request),
        }