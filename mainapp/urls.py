from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('registerpatient/', views.registerpatient, name='registerpatient'),
    path('user-profile/<int:pid1>/', views.user_profile, name='user_profile'),
    path('user-edit-details/<int:pid1>/', views.user_edit_details, name='user_edit_details'),
    path('user-change-password/<int:pid1>/', views.user_change_password, name='user_change_password'),
    path('articles/', views.article, name='articles'),
    path('articles/add', views.add_article, name='add-articles'),
    path('articles/<int:earid>/edit', views.edit_article, name='edit-articles'),
    path('articles/<slug:slug>/', views.single_article, name='single-article'),
    path('hospital-staff/', views.hospital_staff, name='hospital-staff'),
    path('hospital-staff/add', views.add_hospital_staff, name='add-hospital-staff'),
    path('hospital-doctors/', views.hospital_doctors, name='hospital-doctors'),
    path('hospital-doctors/add', views.add_hospital_doctor, name='add-hospital-doctor'),
    path('hospital-patients/', views.hospital_patients, name='hospital-patients'),
    path('hospital-patients/add', views.add_hospital_patient, name='add-hospital-patient'),
    path('deleteptosnotify/<int:ptosid>/', views.deleteptosnotify, name='deleteptosnotify'),
    path('deletestopnotify/<int:stopid>/', views.deletestopnotify, name='deletestopnotify'),
    path('deletestodnotify/<int:stodid>/', views.deletestodnotify, name='deletestodnotify'),
    path('deletedtopnotify/<int:dtopid>/', views.deletedtopnotify, name='deletedtopnotify'),
    path('appointments/', views.appointments, name='appointments'),
    path('appointments/add', views.add_appointment, name='add_appointment'),
    path('appointments/<int:eaid>/edit', views.edit_appointment, name='edit_appointment'),
    path('meeting/<int:aidm>/', views.meeting, name='meeting'),
    path('invite-patient', views.invite_patient, name='invite-patient'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),

]
