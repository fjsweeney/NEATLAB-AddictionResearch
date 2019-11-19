from django.urls import path
from django.urls import include, path
from django.contrib.auth import views as auth_views


from . import views
from . import authentication
from . import modelExecution

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('register', authentication.register, name="register"),
    path('registerPOST', authentication.register_post, name="registerPOST"),
    path('login', authentication.login, name="login"),
    path('loginPOST', authentication.login_post, name="loginPOST"),
    path('logout', authentication.logout, name="logout"),


    #model execution code
    path('models', modelExecution.index, name="modelIndex")



    # path('<int:question_id>/', views.detail, name="detail"),
    # path('<int:question_id>/results/', views.results, name="results"),
    # path('<int:question_id>/vote/', views.vote, name="vote"),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'))
]
