from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

"""
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'scrum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

"""

from django.conf.urls import include, url

from rest_framework.authtoken.views import obtain_auth_token
from board import rest_views
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'task', rest_views.TaskViewSet)
router.register(r'sprint', rest_views.SprintViewSet)
router.register(r'users', rest_views.UserViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api/token/', obtain_auth_token, name='api-token'),

]