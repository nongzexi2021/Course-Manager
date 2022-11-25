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
    cursor.execute('select * from ADVISOR')
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


def adminCourseUpadate(request):
    cursor = connection.cursor();
    if request.method == 'POST':
        id = request.POST['id']
        print(id)
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
    cursor = connection.cursor();
    cursor.execute('select * from USER')
    rows = cursor.fetchall()
    context = {
        "data": rows
    }
    return render(request, 'admin_users.html', context)