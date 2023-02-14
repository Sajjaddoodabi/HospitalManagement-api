import datetime

import jwt
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Doctor, Patient, BaseUser
from accounts.serializers import DoctorSerializer, PatientSerializer


class DoctorRegisterView(APIView):
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
                user = Doctor.objects.create_user(username=username, email=email, password=password)
                user.role = 'DOC'
                user.save()
            except:
                response = {'massage': 'email or username is already taken!'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = DoctorSerializer(user)
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
                user = Patient.objects.create_user(username=username, email=email, password=password)
            except:
                response = {'massage': 'email or username is already taken!'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = PatientSerializer(user)
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
    pass
