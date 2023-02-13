from django.urls import include, path
from rest_framework import routers

from .views import TokenGenerateView, UsersViewSet, auth_signup

app_name = 'users'


router_ver1 = routers.DefaultRouter()
router_ver1.register(r'users', UsersViewSet, basename='user')


urlpatterns = [path('v1/auth/signup/', auth_signup,
                    name='signup'),
               path('v1/auth/token/', TokenGenerateView.as_view(),
                    name='token_obtain_pair'),
               path('v1/', include(router_ver1.urls)),
               ]
