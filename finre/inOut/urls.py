from django.urls import URLPattern, path
from inOut.views import index_view, add_view,item_view

app_name = 'inOut'
urlpatterns = [
    path('', index_view, name='index'),
    path('add/', add_view, name='add'),
    path('view/<str:types>', item_view, name='view')
]