
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Organisation
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, OrganisationSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({
                 "status": "success",
                "message": "Registration successful",
                "data": {
                    "accessToken": token['access'],
                    "user": UserSerializer(user).data
                }
            }, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, email=serializer.data['email'], password=serializer.data['password'])
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({
                    "status": "success",
                    "message": "Login successful",
                    "data": {
                        "accessToken": token['access'],
                        "user": UserSerializer(user).data
                    }
                }, status=status.HTTP_200_OK)
            return Response({"status": "Bad request", "message": "Authentication failed", "statusCode": 401}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"errors": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            if user == request.user or user.organisations.filter(users__in=[request.user]).exists():
                return Response({
                    "status": "success",
             "message": "User data retrieved successfully",
                    "data": UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            return Response({"status": "Forbidden", "message": "Access denied", "statusCode": 403}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"status": "Not Found", "message": "User not found", "statusCode": 404}, status=status.HTTP_404_NOT_FOUND)
class OrganisationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        organisations = request.user.organisations.all()
        serializer = OrganisationSerializer(organisations, many=True)
        return Response({
            "status": "success",
            "message": "Organisations retrieved successfully",
            "data": {"organisations": serializer.data}
        }, status=status.HTTP_200_OK)

class OrganisationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, org_id):
        try:
            organisation = Organisation.objects.get(org_id=org_id)
            if request.user in organisation.users.all():
                serializer = OrganisationSerializer(organisation)
                return Response({
                    "status": "success",
                    "message": "Organisation data retrieved successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            return Response({"status": "Forbidden", "message": "Access denied", "statusCode": 403}, status=status.HTTP_403_FORBIDDEN)
        except Organisation.DoesNotExist:
            return Response({"status": "Not Found", "message": "Organisation not found", "statusCode": 404}, status=status.HTTP_404_NOT_FOUND)
class OrganisationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()
            organisation.users.add(request.user)
            return Response({
                "status": "success",
                "message": "Organisation created successfully",
                "data": OrganisationSerializer(organisation).data
            }, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class AddUserToOrganisationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, org_id):
        try:
            organisation = Organisation.objects.get(org_id=org_id)
            user_id = request.data.get('userId')
            user = User.objects.get(user_id=user_id)
            if request.user in organisation.users.all():
                organisation.users.add(user)
                return Response({
                    "status": "success",
                    "message": "User added to organisation successfully",
                }, status=status.HTTP_200_OK)
            return Response({"status": "Forbidden", "message": "Access denied", "statusCode": 403}, status=status.HTTP_403_FORBIDDEN)
        except Organisation.DoesNotExist:
            return Response({"status": "Not Found", "message": "Organisation not found", "statusCode": 404}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"status": "Not Found", "message": "User not found", "statusCode": 404}, status=status.HTTP_404_NOT_FOUND)
    