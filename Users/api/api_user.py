from  rest_framework.views import  APIView
from rest_framework.response import Response
from  rest_framework import status
from rest_framework.authtoken.models import Token

from  django_otp.plugins.otp_totp.models import  TOTPDevice
from django_otp.oath import TOTP


from Users.serializer import LoginUserSerializer ,ValidateUserserializer
from  Users.models import User


CUSTOMEROLE = 2
class LoginRegisterUser(APIView):
    RETURNDATA = {
        'Success': True
        , 'date': ''
        , 'code': 200
    }

    ExTime=60

    def _create_deviceOtp(self, user):
        device = TOTPDevice.objects.create(user=user,step=self.ExTime)
        device.save()
        totp = TOTP(key=device.bin_key,step=self.ExTime)
        token = totp.token()
        return  token , device

    def post(self,request):
        data = request.data
        serializer = LoginUserSerializer(data=data)
        if  not serializer.is_valid():
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = 'phonr number not valid '
            self.RETURNDATA['code'] = 400
            return Response(self.RETURNDATA, status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(PhoneNumber=data['PhoneNumber'], RoleId_id=CUSTOMEROLE).first()
        if not user :
            user = User.objects.create(PhoneNumber=data['PhoneNumber'], RoleId_id=CUSTOMEROLE)

        otp , device = self._create_deviceOtp(user)
        print(otp)
        self.RETURNDATA['Success'] = False
        self.RETURNDATA['date'] = {
            'key':device.key,
            'user_name': data['PhoneNumber'],
            'ExTime': self.ExTime
        }
        self.RETURNDATA['code'] = 200
        return Response(self.RETURNDATA, status.HTTP_200_OK)



class ValidateUser(APIView):
    RETURNDATA = {
        'Success': True
        , 'date': ''
        , 'code': 200
    }

    def post(self,request):
        data = request.data
        serializer = ValidateUserserializer(data=data)
        if not serializer.is_valid():
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = 'otp not valid '
            self.RETURNDATA['code'] = 400
            return Response(self.RETURNDATA, status.HTTP_400_BAD_REQUEST)

        device = TOTPDevice.objects.filter(key=data.get('key')).first()
        if not device:
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = 'device not valid '
            self.RETURNDATA['code'] = 400
            return Response(self.RETURNDATA, status.HTTP_400_BAD_REQUEST)

        validate = device.verify_token(data['otp'])
        if not  validate:
            self.RETURNDATA['Success'] = False
            self.RETURNDATA['date'] = 'otp monghazi not valid '
            self.RETURNDATA['code'] = 400
            return Response(self.RETURNDATA, status.HTTP_400_BAD_REQUEST)

        user = device.user

        token = Token.objects.create(user=user)
        token_key = token.key

        self.RETURNDATA['date'] = {'token': token_key}
        self.RETURNDATA['code'] = 200
        self.RETURNDATA['Success'] = True

        return Response(self.RETURNDATA, status.HTTP_200_OK)





