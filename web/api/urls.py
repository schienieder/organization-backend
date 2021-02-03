from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from api.views import CreateAccount
from api.views import UpdateAccount
from api.views import RetriveAccount
from api.views import GetUserInfo
from api.views import UpdateUserInfo
from api.views import CreateOrganization
from api.views import UpdateOrganization
from api.views import DeleteOrganization
from api.views import RetriveOrganization

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path(
        "auth/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "auth/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    # MYUSER MODEL SERIALIZERS AND VIEWS
    # DONE
    # DONE
    # DONE
    path("api/acc/create/", CreateAccount.as_view(), name="createAccount"),
    path("api/acc/get/<int:pk>", RetriveAccount.as_view(), name="accGet"),
    path("api/acc/update/", UpdateAccount.as_view(), name="accUpdate"),
    # USER INFO MODELS AND VIEWS
    # DONE
    # DONE
    path("api/info/get/<int:pk>", GetUserInfo.as_view(), name="accInfoGet"),
    path("api/info/update/", UpdateUserInfo.as_view(), name="accInfoUpdate"),
    #
    #
    #
    path("api/org/create/", CreateOrganization.as_view(), name="orgCreate"),
    path("api/org/update/", UpdateOrganization.as_view(), name="orgUpdate"),
    path("api/org/destroy/", DeleteOrganization.as_view(), name="orgDestroy"),
    path("api/org/get/<int:pk>", RetriveOrganization.as_view(), name="orgGet"),
]
