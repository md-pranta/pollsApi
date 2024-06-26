from rest_framework.views import APIView
from rest_framework import generics,status,viewsets
from rest_framework.response import Response
from django.shortcuts import get_list_or_404
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied 

#local
from .models import Poll, Choice
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer,UserSerializer

class LoginView(APIView):
    permission_classes = ()
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token":user.auth_token.key})
        else:
            return Response({"error": "wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class=UserSerializer



class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    
    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])
        if request.user != poll.created_by:
            raise PermissionDenied("you can not delete this Post")
        return super().destroy(request, *args, **kwargs)()



# class PollList(generics.ListCreateAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer


# class PollDetail(generics.RetrieveDestroyAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer


class ChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        q = Choice.objects.filter(poll_id=self.kwargs["pk"])
        return q
    serializer_class = ChoiceSerializer
    
    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])
        if not request.user == poll.created_by:
            raise PermissionDenied("You can not create choice for this poll.")
        return super().post(request, *args, **kwargs)


class CreateVote(generics.CreateAPIView):
    serializer_class = VoteSerializer
    
    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# full control over views


# class PollList(APIView):
#     def get(self,request):
#         polls = Poll.objects.all()
#         data = PollSerializer(polls,many=True).data
#         return Response(data)
# class PollDetail(APIView):
#     def get(self, request, pk):
#         poll = get_list_or_404(Poll, pk=pk)
#         data = PollSerializer(Poll).data
#         return Response(data)
