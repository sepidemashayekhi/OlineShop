from   django.urls import  path
from  Users.api.api_adminUser import RegisterUser, ResetPassword, Login, ResetPasswordUrl
from Users.api.api_user import LoginRegisterUser, ValidateUser

urlpatterns = [
        path('AdminUser/register', RegisterUser.as_view(), name='RegisterUser'),
        path('AdminUser/login', Login.as_view()),
        path('AdminUser/resetpass', ResetPassword.as_view()),
        path('AdminUser/<str:token>/<int:otp>', ResetPasswordUrl.as_view()),

        path('user/login', LoginRegisterUser.as_view()),
        path('user/validate', ValidateUser.as_view())
        ]
