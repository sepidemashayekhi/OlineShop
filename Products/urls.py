from   django.urls import  path
from Products.api.apis import CreateProduct

urlpatterns=[
        path('Product',CreateProduct.as_view(),name='ProductView'),
]