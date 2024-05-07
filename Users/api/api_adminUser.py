from rest_framework.views import APIView
from  rest_framework.response import Response
from  rest_framework import  status
from rest_framework.authtoken.models import Token

from  django_otp.plugins.otp_totp.models import  TOTPDevice
from django_otp.oath import TOTP

from  Users.serializer import RegisterUserSerializer,ValidateUserserializer,ResendOtpSerializer,LoginSerializer , UrlSerializer
from  Users.models import User,Rols
from shop import settings

import  os


CUSTOMERROLE = 2
VALIDSTATE = 'validated'

class RegisterUser(APIView):
    RETURNDATA = {
        'Success': True
        ,'date':''
        ,'code':200
    }
    def _create_deviceOtp(self, user):
        device = TOTPDevice.objects.create(user=user,step=60)
        device.save()
        totp = TOTP(key=device.bin_key,step=60)
        token = totp.token()
        return  token , device

    def _send_sms(self, token):
        pass

    def post(self,request):
        data = request.data
        data['state'] = 'not_validated'
        serializer = RegisterUserSerializer(data=data)
        if not serializer.is_valid():
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = 'invalid json'
            self.RETURNDATA['code'] = 400
            return Response(data=self.RETURNDATA, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data

        checkuser = User.objects.filter(PhoneNumber=data['PhoneNumber'], state='validated').first()
        if checkuser:
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = 'phone number is repited'
            self.RETURNDATA['code'] = 400
            return Response(data=self.RETURNDATA, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(first_name=data['first_name'], last_name=data['last_name'],
                    email=data['email'], RoleId=Rols.objects.get(id=CUSTOMERROLE), PhoneNumber=data['PhoneNumber'],
                                   state=data['state'], password=data['password'])

        token, device = self._create_deviceOtp(user)
        #self.send_sms(token)
        print(token)

        self.RETURNDATA['Success'] = True
        self.RETURNDATA['date'] = {'KEY' : device.key,
                                   'user_name' : user.PhoneNumber}
        self.RETURNDATA['code'] = 200
        return  Response(data=self.RETURNDATA,status=status.HTTP_201_CREATED)

    def put(self,request):

        data = request.data
        serializer = ValidateUserserializer(data=data)
        if not  serializer.is_valid():
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = 'vorodi valid nist'
            self.RETURNDATA['code'] = 400
            return Response(self.RETURNDATA, status.HTTP_400_BAD_REQUEST)

        otp_token = data.get('otp')
        device_key = data.get('key')


        device = TOTPDevice.objects.filter(key=device_key).first()
        if not device:
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = 'user not valid'
            self.RETURNDATA['code'] = 400
            return  Response(self.RETURNDATA,status.HTTP_400_BAD_REQUEST)

        validation = device.verify_token(otp_token)
        if not validation:
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = 'token not valid'
            self.RETURNDATA['code'] = 400
            return  Response(self.RETURNDATA,status.HTTP_400_BAD_REQUEST)

        user = device.user
        user.state = VALIDSTATE
        user.save()

        token = Token.objects.create(user=user)
        token_key = token.key

        self.RETURNDATA['date']= {'token':token_key}
        self.RETURNDATA['code'] = 200
        self.RETURNDATA['Success'] =True

        return  Response(self.RETURNDATA,status.HTTP_200_OK)

    def get(self,request):
        data = request.GET
        serializer = ResendOtpSerializer(data=data)

        if not  serializer.is_valid():
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = 'vorodi valid nist'
            self.RETURNDATA['code'] = 400
            return Response(self.RETURNDATA, status.HTTP_400_BAD_REQUEST)

        user_name = User.objects.filter(PhoneNumber=request.GET.get('PhoneNumber')).order_by('id').last()
        if not  user_name:
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = 'user not have'
            self.RETURNDATA['code'] = 400
            return Response(self.RETURNDATA, status.HTTP_400_BAD_REQUEST)

        token ,device = self._create_deviceOtp(user_name)
        print(token)
        self.RETURNDATA['Success'] = True
        self.RETURNDATA['date'] = {'KEY': device.key,
                                   'user_name': user_name.PhoneNumber}
        self.RETURNDATA['code'] = 200
        return Response(data=self.RETURNDATA, status=status.HTTP_201_CREATED)


class Login(APIView):
    RETURNDATA = {
        'Success': True
        , 'date': ''
        , 'code': 200
    }
    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = serializer.error_messages
            self.RETURNDATA['code'] = 400
            return Response(data=self.RETURNDATA, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(PhoneNumber=data['PhoneNumber'],password=data['password'],state = VALIDSTATE)
        except:
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = 'password and phoneNumber is not valid'
            self.RETURNDATA['code'] = 400
            return Response(data=self.RETURNDATA, status=status.HTTP_400_BAD_REQUEST)

        token = Token.objects.filter(user=user).first()
        if not token:
            token = Token.objects.create(user=user)
        token_key = token.key

        self.RETURNDATA['date'] = {'token': token_key}
        self.RETURNDATA['code'] = 200
        self.RETURNDATA['Success'] = True

        return Response(self.RETURNDATA, status.HTTP_200_OK)


class ResetPassword(APIView):
    RETURNDATA = {
        'Success': True
        , 'date': None
        , 'code': 200
    }
    def _create_deviceOtp(self, user):
        device = TOTPDevice.objects.create(user=user,step=120)
        device.save()
        totp = TOTP(key=device.bin_key)
        token = totp.token()
        return  token , device

    def get(self,request):
        data = request.GET.dict()
        serializer = ResendOtpSerializer(data=data)
        if not serializer.is_valid():
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = serializer.error_messages
            self.RETURNDATA['code'] = 400
            return Response(data=self.RETURNDATA, status=status.HTTP_400_BAD_REQUEST)
        # try:
        user = User.objects.filter(PhoneNumber=data['PhoneNumber']).first()
        if not user:
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = 'not user'
            self.RETURNDATA['code'] = 400
            return Response(data=self.RETURNDATA, status=status.HTTP_400_BAD_REQUEST)

        otp_code , device = self._create_deviceOtp(user)
        url = os.path.join(settings.DEPLOY_HOST,'user',str(device.key),str(otp_code))

        print(url)
        # send sms

        self.RETURNDATA['date'] = None
        self.RETURNDATA['code'] = 200
        self.RETURNDATA['Success'] = True

        return Response(self.RETURNDATA, status.HTTP_200_OK)


class ResetPasswordUrl(APIView):
    RETURNDATA = {
        'Success': True
        , 'date': None
        , 'code': 200
    }
    def post(self,request,token,otp):
        data = {
            'otp':otp,
            'token':token,
            'password':request.data.get('password')
        }
        serializer = UrlSerializer(data=data)
        if not serializer.is_valid():
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = 'vordi not valid'
            self.RETURNDATA['code'] = 400
            return Response(data=self.RETURNDATA, status=status.HTTP_400_BAD_REQUEST)

        device = TOTPDevice.objects.filter(key=token).first()
        if not device:
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = 'not user'
            self.RETURNDATA['code'] = 400
            return Response(data=self.RETURNDATA, status=status.HTTP_400_BAD_REQUEST)
        validate = device.verify_token(otp)
        if not validate:
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = 'link not vlid'
            self.RETURNDATA['code'] = 400
            return Response(data=self.RETURNDATA, status=status.HTTP_400_BAD_REQUEST)
        user = device.user

        user.password = request.data['password']
        user.save()

        token = Token.objects.filter(user=user).first()
        if not token:
            token = Token.objects.create(user=user)
        token_key = token.key

        self.RETURNDATA['date'] = {'token': token_key}
        self.RETURNDATA['code'] = 200
        self.RETURNDATA['Success'] = True

        return Response(self.RETURNDATA, status.HTTP_200_OK)







