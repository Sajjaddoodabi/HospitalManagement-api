import datetime

import jwt
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import RetrieveUpdateDestroyAPIView, UpdateAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from Hospital.models import AppointmentTime
from Hospital.serializers import AppointmentTimeSerializer
from accounts.models import Doctor, Patient, BaseUser, DoctorCategory
from accounts.serializers import DoctorSerializer, PatientSerializer, UserSerializer, ChangePasswordSerializer, \
    DoctorMiniSerializer, DoctorCategorySerializer


class DoctorRegisterView(APIView):
    def post(self, request):
        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            category = request.data['category']
            category = DoctorCategory.objects.get(title=category)
        except:
            response = {'massage': 'field error'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            if not username:
                response = {'massage': 'username field required!'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            if not email:
                response = {'massage': 'email field required!'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            if not password:
                response = {'massage': 'password field required!'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            if not category:
                response = {'massage': 'category field required!'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = BaseUser.objects.create_user(username=username, email=email, password=password)
                user.role = 'DOC'
                user.save()
                doctor = Doctor.objects.create(parent_user_id=user.id, category=category)
            except Exception as e:
                response = {'massage': str(e)}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = DoctorSerializer(doctor)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            # serializer = DoctorSerializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
            # return Response(serializer.data)


class PatientRegisterView(APIView):
    def post(self, request):
        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
        except:
            response = {'massage': 'field error'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            if not username:
                response = {'massage': 'username field required!'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            if not email:
                response = {'massage': 'email field required!'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            if not password:
                response = {'massage': 'password field required!'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = BaseUser.objects.create_user(username=username, email=email, password=password)
                patient = Patient.objects.create(parent_user_id=user.id)
            except Exception as e:
                response = {'massage': str(e)}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = PatientSerializer(patient)
                return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = BaseUser.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('User not found!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        #
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        #
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'massage': 'logged out successfully'
        }

        return response


class ChangePassword(APIView):
    def put(self, request):
        user = get_user(request)
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            current_password = serializer.current_password
            new_password = serializer.new_password
            if user.check_password(current_password):
                if current_password != new_password:
                    user.password = make_password(new_password)
                    user.save()
                    serializer = UserSerializer(user)
                    return Response(serializer.data)

                response = {'massage': 'U should use a new password'}
                return Response(response)

            response = {'massage': 'wrong password'}
            return Response(response)

        return Response(serializer.errors)


class UserView(APIView):
    def get(self, request):
        user = get_user(request)
        if not user:
            raise AuthenticationFailed('User not found!')

        if user.role == 'PAT':
            patient = Patient.objects.filter(parent_user_id=user.id).first()
            serializer = PatientSerializer(patient)
        elif user.role == 'DOC':
            doctor = Doctor.objects.filter(parent_user_id=user.id).first()
            serializer = DoctorSerializer(doctor)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


def get_user(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    user = BaseUser.objects.filter(id=payload['id']).first()

    return user


class DoctorDetail(RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.filter(parent_user__status=True)
    serializer_class = DoctorSerializer


class PatientDetail(RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.filter(parent_user__status=True)
    serializer_class = PatientSerializer


class AddDoctorCategory(CreateAPIView):
    queryset = DoctorCategory.objects.all()
    serializer_class = DoctorCategorySerializer


class DoctorCategoryDetail(APIView):
    def get(self, request, pk):
        category = DoctorCategory.objects.filter(pk=pk).first()
        if category is not None:
            serializer = DoctorCategorySerializer(category)
            return Response(serializer.data)
        else:
            response = {'massage': 'category does not exist!'}
            return Response(response)

    def put(self, request, pk):
        category = DoctorCategory.objects.get(pk=pk)
        serializer = DoctorCategorySerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.data['title']
            is_Exist = DoctorCategory.objects.filter(title=title).exists()
            if is_Exist:
                response = {'massage': 'category with this name already exist!'}
                return Response(response)
            category.title = title
            category_ser = DoctorCategorySerializer(category)
            return Response(category_ser.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        category = DoctorCategory.objects.filter(pk=pk).first()
        if category is not None:
            category.delete()
            response = {'massage': f'category with id {category.id} deleted successfully!'}
            return Response(response)

        response = {'massage': 'category does not exist!'}
        return Response(response)


class DoctorCategories(ListAPIView):
    queryset = DoctorCategory.objects.filter(is_active=True)
    serializer_class = DoctorCategorySerializer


class AppointmentTimeDetail(RetrieveUpdateDestroyAPIView):
    queryset = AppointmentTime.objects.all()
    serializer_class = AppointmentTimeSerializer
