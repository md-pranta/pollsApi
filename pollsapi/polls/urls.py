from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import ChoiceList,CreateVote,PollViewSet,UserCreate,LoginView


router = DefaultRouter()
router.register('polls',PollViewSet, basename='polls')

urlpatterns = [
    # path('',include(router.urls)),
    path("choices/", ChoiceList.as_view(), name="choice_list"),
    path("login/", LoginView.as_view(), name="login"),
    path("users/", UserCreate.as_view(), name="user_create"),
    path("vote/", CreateVote.as_view(), name="create_vote"),
    path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choice_list"),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),

]

urlpatterns += router.urls