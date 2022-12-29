from django.urls import path


from . import views


urlpatterns = [
    path('', views.redirect_to_home_customize, name='redirect_to_login_customize'),
    path('signup/', views.SignUpView.as_view(), name="signup"),
]




