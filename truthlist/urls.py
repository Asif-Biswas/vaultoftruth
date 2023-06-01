from django.urls import path 
from. import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('upload/', views.upload, name='upload'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.logout_view,name='logout'),

    path('assessment/', views.assessment, name='assessment'),
    path('add_to_certificate/<int:id>/<str:value>/', views.add_to_certificate, name='add_to_certificate'),
    path('add-new-question/', views.add_new_question, name='add_new_question'),
    path('pending-questions/', views.pending_questions, name='pending_questions'),
    path('approve-question/<int:id>/', views.approve_question, name='approve_question'),
    path('reject-question/<int:id>/', views.reject_question, name='reject_question'),
    path('public-believes/', views.public_believes, name='public_believes'),
    path('reasons/<int:id>/', views.reasons, name='reasons'),
]
