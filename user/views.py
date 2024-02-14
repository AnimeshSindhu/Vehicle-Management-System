from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vehicle
from .serializers import UserRegistrationSerialization, UserLoginSerializer, CustomTokenObtainPairSerializer, \
    VehicleSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView


class UserRegistrationView(GenericAPIView):
    serializer_class = UserRegistrationSerialization

    def post(self, request):
        serializer = UserRegistrationSerialization(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            refresh = CustomTokenObtainPairSerializer.get_token(user)
            return Response({'refresh': str(refresh),
                             'access': str(refresh.access_token), 'msg': 'Registration Successful'})
        return Response(serializer.errors)


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                refresh = CustomTokenObtainPairSerializer.get_token(user)
                return Response({'refresh': str(refresh),
                                 'access': str(refresh.access_token), 'msg': 'Login Successful'})
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}})


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = {
            'id': user.id,
            'username': user.name,
            'email': user.email,
            'role': user.role
        }
        return Response(user_data)


class VehicleListCreate(ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class VehicleView(GenericAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        vehicles = Vehicle.objects.filter(user=user)
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)


class UserChangePasswordView(GenericAPIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response("Password Changed Successfully")
        else:
            return Response(serializer.errors)


class SendPasswordResetEmailView(GenericAPIView):
    serializer_class = SendPasswordResetEmailSerializer

    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Reset link send. Please check your Email'})


class UserPasswordResetView(GenericAPIView):
    serializer_class = UserPasswordResetSerializer

    def post(self, request, uid, token):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response("Password Reset Successfully")
        else:
            return Response(serializer.errors)


class RoleBasedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == 'admin':
            vehicles = Vehicle.objects.all()
            serializer = VehicleSerializer(vehicles, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'Not an admin Member'})

    def put(self, request, pk):
        user = request.user
        if user.role == 'admin':
            vehicle = Vehicle.objects.get(pk=pk)
            serializer = VehicleSerializer(vehicle, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({'message': 'Not an admin user'})

    def patch(self, request, pk):
        user = request.user
        if user.role == 'admin':
            vehicle = Vehicle.objects.get(pk=pk)
            serializer = VehicleSerializer(vehicle, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        else:
            return Response({'message': 'Not an admin user'})

    def delete(self, request, pk):
        user = request.user
        if user.role == 'admin':
            vehicle = Vehicle.objects.get(pk=pk)
            vehicle.delete()
            return Response({'message': 'Vehicle deleted successfully'})
        else:
            return Response({'message': 'Not an admin user'})
