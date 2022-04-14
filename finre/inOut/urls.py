from unicodedata import name
from django.urls import URLPattern, path
from inOut.views import index_view, add_view,item_view,delete_view, logout_view, login_view, register_view, edit_view

app_name = 'inOut'
urlpatterns = [
    path('', index_view, name='index'),
    path('view/<str:types>/', item_view, name='view'),
    path('view/<str:types>/add/', add_view, name='add'),
    path('delete/<str:types>/<int:id>', delete_view, name='delete'),
    path('edit/<str:types>/<int:id>', edit_view, name='edit'),
    path('logout/', logout_view, name='logout' ),
    path('login/', login_view, name='login'),
    path('signUp/', register_view, name='signUp')
]