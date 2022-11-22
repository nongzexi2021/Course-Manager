from django.shortcuts import render

# Create your views here.
from .models import Employee
from .models import Orders
from decimal import Decimal

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import connection


def homePage(request):
    return render(request, 'home.html')

def loginPage(request):
    return render(request, 'loginPage.html')

def profilePage(request):
    return render(request, 'profilePage.html')

def billingPage(request):
    return render(request, 'billingPage.html')

def courseList(request):
    return render(request, 'courseList.html')

def adminCourse(request):
    return render(request, 'admin_course.html')

def adminHome(request):
    return render(request, 'admin_home.html')

def adminProfile(request):
    return render(request, 'admin_profile.html')

def adminUsers(request):
    return render(request, 'admin_users.html')

def advisorStudents(request):
    return render(request, 'advisor_students.html')

def advisorHome(request):
    return render(request, 'advisor_home.html')

def advisorProfile(request):
    return render(request, 'advisor_profile.html')

# list all advisor
def listAdvisorSql(request):
    cursor = connection.cursor();
    cursor.execute('select * from ADVISOR')
    rows = cursor.fetchall()
    context = {
        "data" : rows
    }

    return render(request, 'advisorList.html', context)