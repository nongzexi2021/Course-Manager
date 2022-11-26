"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webApp import views

urlpatterns = [
    #path("admin/", admin.site.urls),
    path('home', views.homePage),
    path('', views.loginPage),
    path('profile', views.profilePage),
    path('billing', views.billingPage),
    path('list', views.courseList),
    path('enroll', views.listAllCourseSql),
    path('advisorList', views.listAdvisorSql),
    path('admin/course', views.adminCourse),
    path('admin/home', views.adminHome),
    path('admin/profile', views.adminProfile),
    path('advisor/profile', views.advisorProfile),
    path('advisor/student', views.advisorStudents),
    path('advisor/home', views.advisorHome),
    path('admin/create', views.adminCourseCreate),
    path('admin/inserted', views.adminCourseAddProcess),
    path('admin/course/delete/<int:id>', views.adminCourseDeleteProcess),
    path('admin/<int:id>', views.adminCourseEdit),
    path('admin/course/edit/update', views.adminCourseUpadate),
    path('admin/users', views.listUserSql)
]
