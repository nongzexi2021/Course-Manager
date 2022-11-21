from django.shortcuts import render



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

def advisorList(request):
    return render(request, 'advisorList.html')

def adminCourse(request):
    return render(request, 'admin_course.html')

def adminHome(request):
    return render(request, 'admin_home.html')

def adminProfile(request):
    return render(request, 'admin_profile.html')

def adminUsers(request):
    return render(request, 'admin_users.html')