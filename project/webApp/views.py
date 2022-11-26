from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
import mysql.connector
from django.db import connection

mydb = mysql.connector.connect(
    host="35.197.108.217",
    user="root",
    password="nongzexi",
    database="group7"
)


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


def enrollCourse(request):
    return render(request, 'enrollPage.html')


def adminCourse(request):
    cursor = connection.cursor();
    cursor.execute('select * from COURSE')
    rows = cursor.fetchall()
    context = {
        "data": rows
    }
    return render(request, 'editCourse.html', context)


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
    cursor.execute('select * from USER where role="advisor"')
    rows = cursor.fetchall()
    context = {
        "data": rows
    }
    return render(request, 'advisorList.html', context)


def listAllCourseSql(request):
    cursor = connection.cursor();
    cursor.execute("select * from `COURSE`")
    rows = cursor.fetchall()
    context = {
        "data": rows
    }
    return render(request, 'enrollPage.html', context)


def adminCourseCreate(request):
    return render(request, 'admin_addCourse.html')


def adminCourseAddProcess(request):
    cursor = connection.cursor();
    if request.method == 'POST':
        courseName = request.POST['name']
        proID = request.POST['professor_id']
        start_date = request.POST['start_date']
        duration = request.POST['duration']
        room_id = request.POST['room_id']
        college_id = request.POST['college_id']
        credit = request.POST['credit']
        sql = "INSERT INTO COURSE (name, professor_id, start_date, duration, room_id, college_id, credit) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (courseName, proID, start_date, duration, room_id, college_id, credit)
        cursor.execute(sql, val)
        mydb.commit()
        return redirect(adminCourse)
    else:
        return redirect(adminCourse)


def adminCourseDeleteProcess(request, id):
    cursor = connection.cursor();
    cursor.execute(f'delete from `COURSE` where `course_id` = {id}')
    mydb.commit()
    return redirect(adminCourse)


def adminCourseEdit(request, id):
    cursor = connection.cursor();
    cursor.execute(f'select * from `COURSE` where `course_id` = {id}')
    row = cursor.fetchone()
    context = {
        "data": row
    }
    return render(request, "edit.html", context)


def adminCourseUpadate(request, id):
    cursor = connection.cursor();
    if request.method == 'POST':
        courseName = request.POST['name']
        proID = request.POST['professor_id']
        start_date = request.POST['start_date']
        duration = request.POST['duration']
        room_id = request.POST['room_id']
        college_id = request.POST['college_id']
        credit = request.POST['credit']
        cursor.execute("""
           UPDATE COURSE
           SET name=%s, professor_id=%s, start_date=%s, duration=%s, room_id=%s, college_id=%s, credit=%s
           WHERE course_id=%s
        """, (courseName, proID, start_date, duration, room_id, college_id, credit, id))
        mydb.commit()
        return redirect(adminCourse)
    else:
        return redirect(adminCourse)


def listUserSql(request):
    cursor = connection.cursor()
    cursor.execute('select * from USER')
    rows = cursor.fetchall()
    print(rows)
    context = {
        "data": rows
    }
    return render(request, 'admin_users.html', context)


def listOneUserSql(request):
    cursor = connection.cursor()
    cursor.execute('select * from USER')
    rows = cursor.fetchone()
    print(rows)
    context = {
        "data": rows
    }
    return render(request, 'admin_updateUser.html', context)


def adminUserCreate(request):
    return render(request, 'admin_addUser.html')


def adminUserAddProcess(request):
    cursor = connection.cursor();
    if request.method == 'POST':
        userAccount = request.POST['account']
        password = request.POST['password']
        username = request.POST['username']
        firstName = request.POST['first_name']
        lastName = request.POST['last_name']
        role = request.POST['role']
        location = request.POST['location']
        email = request.POST['email']
        phone = request.POST['phone']
        major = request.POST['major']
        sql = "INSERT INTO USER (useraccount, password, username, first_name, last_name, role, location, email, phone, login, major) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (userAccount, password, username, firstName, lastName, role, location, email, phone, False, major)
        cursor.execute(sql, val)
        mydb.commit()
        return redirect(listUserSql)
    else:
        return redirect(listUserSql)


def adminUserEdit(request, id):
    cursor = connection.cursor();
    cursor.execute(f'select * from `USER` where `user_id` = {id}')
    row = cursor.fetchone()
    context = {
        "data": row
    }
    return render(request, "admin_updateUser.html", context)


def adminUserUpdate(request, id):
    cursor = connection.cursor();
    if request.method == 'POST':
        userAccount = request.POST['account']
        password = request.POST['password']
        username = request.POST['username']
        firstName = request.POST['first_name']
        lastName = request.POST['last_name']
        role = request.POST['role']
        location = request.POST['location']
        email = request.POST['email']
        phone = request.POST['phone']
        cursor.execute("""
               UPDATE USER
               SET useraccount=%s, password=%s, username=%s, first_name=%s, last_name=%s, role=%s, location=%s, email=%s, phone=%s
               WHERE user_id=%s
            """, (userAccount, password, username, firstName, lastName, role, location, email, phone, id))
        mydb.commit()
        return redirect(listUserSql)
    else:
        return redirect(listUserSql)


def adminUserDeleteProcess(request, id):
    cursor = connection.cursor()
    cursor.execute(f'delete from `USER` where `user_id` = {id}')
    mydb.commit()
    return redirect(listUserSql)

def listOneUserProfile(request):
    cursor = connection.cursor()
    cursor.execute('select * from `USER` where `login`=1')
    rows = cursor.fetchone()
    context = {
        "data": rows
    }
    return render(request, 'admin_profile.html', context)

def listOneUserProfileStudent(request):
    cursor = connection.cursor()
    cursor.execute('select * from `USER` where `login`=1')
    rows = cursor.fetchone()
    context = {
        "data": rows
    }
    return render(request, 'profilePage.html', context)

def listOneUserProfileAdvisor(request):
    cursor = connection.cursor()
    cursor.execute('select * from `USER` where `login`=1')
    rows = cursor.fetchone()
    context = {
        "data": rows
    }
    return render(request, 'advisor_profile.html', context)
