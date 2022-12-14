from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
import mysql.connector
from django.db import connection
from django.db import Error
from .models import User
from .models import CourseRegistration
from .models import Course
from django.contrib.auth import authenticate, login
from .models import User
from django.http import HttpResponseRedirect
import random

mydb = mysql.connector.connect(
    host="35.197.108.217", user="root", password="nongzexi", database="group7"
)


def get_uniqueID(request):
    uniqueID = request.COOKIES.get("uniqueID")
    return uniqueID


def get_user_role(request):
    uniqueID = get_uniqueID(request)
    cursor = connection.cursor()
    cursor.execute(f"select * from `USER` where uniqueID={uniqueID}")
    user = cursor.fetchone()
    return user[6]


def homePage(request):
    # show the current student dashboard data from the database
    uniqueID = request.COOKIES.get("uniqueID")
    cursor = connection.cursor()
    cursor.execute(f"select * from `USER` where uniqueID={uniqueID}")
    user = cursor.fetchone()
    if user[6] == "student":
        cursor.execute(f"select * from `STUDENTS` where student_id={uniqueID}")
        student = cursor.fetchone()
        context = {"user": student}
    else:
        context = {"user": user}

    def favouriteCourse(cursor, limit):

        cursor.execute(
            f"SELECT COURSE_REGISTRATION.course_id, COUNT(COURSE_REGISTRATION.course_id) AS num, COURSE.name\
                        FROM COURSE_REGISTRATION\
                        INNER JOIN COURSE\
                        ON COURSE_REGISTRATION.course_id = COURSE.course_id\
                        GROUP BY COURSE_REGISTRATION.course_id\
                        ORDER BY num DESC\
                        LIMIT {limit};"
        )
        courses = cursor.fetchall()
        return courses

    top3Courses = favouriteCourse(cursor, 3)
    context["top"] = top3Courses

    cursor.close()

    return render(request, "home.html", context)


def logout(request):
    response = HttpResponseRedirect("/")
    response.delete_cookie("uniqueID")
    return response


def loginPage(request):
    return render(request, "loginPage.html")


def registerPage(request):
    cursor = connection.cursor()
    cursor.execute("select * from MAJOR")
    rows = cursor.fetchall()
    context = {"data": rows}
    return render(request, "registerPage.html", context)


def registerUser(request):
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    first_name = request.POST.get("first name", "default first name")
    last_name = request.POST.get("last name", "default last name")
    email = request.POST.get("email", "default email")
    role = request.POST.get("role", "student")
    location = request.POST.get("location", "bay area")
    phone = request.POST.get("phone", "000-000-0000")
    major = request.POST.get("major", "Computer Science")

    uniqueID = ""
    if role != "student":
        uniqueID = (str)(random.randrange(10000, 20000))
    else:
        uniqueID = (str)(random.randrange(20000, 30000))

    if username and password:
        try:
            if role == "student":
                name = first_name + " " + last_name
                sql = (
                    "INSERT INTO STUDENTS (student_id, name, major, billing_balance, GPA, advisor_id, credit_limits) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                )
                val = (uniqueID, name, major, 0, None, 400, 9)
                cursor = connection.cursor()
                cursor.execute(sql, val)
            elif role == "advisor":
                name = first_name + " " + last_name
                sql = (
                    "INSERT INTO ADVISORS (employee_id, name, major_id) "
                    "VALUES (%s, %s, %s)"
                )
                val = (
                    uniqueID,
                    name,
                    major,
                )
                cursor = connection.cursor()
                cursor.execute(sql, val)
            User.objects.create_user(
                username,
                password,
                uniqueID,
                first_name,
                last_name,
                email,
                role,
                location,
                phone,
                major,
            )
        except Error as e:
            print("Error while connecting to MySQL", e)
    else:
        return redirect("login")  # ???????????????????????????

    return redirect("login")


def checkLogin(request):
    print(request.body)
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    user = authenticate(request, username=username, password=password)
    if user is not None:

        login(request, user)
        id = User.objects.get(username=username).uniqueID
        role = User.objects.get(username=username).role
        response = None
        print(role)
        if role == "student":
            response = redirect("home")
        elif role == "admin":
            response = redirect("admin")
        else:
            response = redirect("advisor")

        response.set_cookie("uniqueID", id, max_age=12 * 3600)
        return response
    else:
        print("\n *** login fail -- user does not exist! *** \n")
        return redirect("login")


def profilePage(request):
    return render(request, "profilePage.html")


def billingPage(request):
    return render(request, "billingPage.html")


def courseList(request):
    id = (int)(request.COOKIES.get("uniqueID"))
    allCourse = CourseRegistration.objects.filter(student_id=id)
    res = []
    count_credits = 0
    for o in allCourse:
        c = Course.objects.get(course_id=o.course_id)
        res.append(c)
        count_credits += c.credit
    context = {"allCourse": res, "total_credits": count_credits}
    return render(request, "courseList.html", context)


def enrollCourse(request):
    return render(request, "enrollPage.html")


def adminCourse(request):
    cursor = connection.cursor()
    cursor.execute("select * from COURSE")
    rows = cursor.fetchall()
    context = {"data": rows}
    return render(request, "editCourse.html", context)


def adminHome(request):
    uniqueID = request.COOKIES.get("uniqueID")
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT major\
              FROM USER\
              WHERE uniqueID = {uniqueID};"
    )
    major = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT location\
              FROM USER\
              WHERE uniqueID = {uniqueID};"
    )
    location = cursor.fetchone()[0]
    cursor.execute(
        f"SELECT first_name, last_name, uniqueID, COUNT(*) AS num\
                FROM USER\
                INNER JOIN COURSE_REGISTRATION\
                ON USER.uniqueID = COURSE_REGISTRATION.student_id\
                WHERE major = '{major}'\
                GROUP BY uniqueID\
                HAVING num < 2;"
    )
    students = cursor.fetchall()
    context = {"creditLessThanEight": students}
    return render(request, "admin_home.html", context)


def adminProfile(request):
    return render(request, "admin_profile.html")


def adminUsers(request):
    return render(request, "admin_users.html")


def advisor_students(request):
    if get_user_role(request) != "advisor":
        return redirect("login")
    cursor = connection.cursor()
    uniqueID = get_uniqueID(request)
    if uniqueID == None:
        redirect("login")
    cursor.execute(
        f"select * from MAJOR m left join "
        f"(select * from STUDENTS where major=(select major_id from ADVISORS where employee_id = {uniqueID})) stu "
        f"on m.major_id=stu.major where student_id is not null"
    )
    students = cursor.fetchall()
    context = {"students": students}
    return render(request, "advisor_students.html", context)


def advisor_edit_student(request, student_id):
    # get the selected student info
    if get_user_role(request) != "advisor":
        return redirect("login")
    cursor = connection.cursor()
    cursor.execute(f"select * from STUDENTS where student_id = {student_id}")
    student = cursor.fetchone()

    cursor.execute(f"select * from USER where uniqueID = {student_id}")
    info = cursor.fetchone()

    context = {"student": student, "info": info}
    return render(request, "advisor_edit_student.html", context)


def advisor_save_student(request, student_id):
    if get_user_role(request) != "advisor":
        return redirect("login")
    cursor = connection.cursor()
    if request.method == "POST":
        location = request.POST["location"]
        credit_limit = request.POST["creditLimit"]
        # save user location
        _id = str(student_id)
        cursor.execute(
            """UPDATE USER SET location=%s WHERE uniqueID=%s""",
            (location, _id),
        )
        # save student credit limit
        cursor.execute(
            """UPDATE STUDENTS SET credit_limits=%s WHERE student_id=%s """,
            (credit_limit, _id),
        )
        mydb.commit()
    return redirect(advisor_students)


def creditLessThanEight(employee_id, uniqueID, cursor):
    cursor.execute(
        f"SELECT major_id\
              FROM ADVISORS\
              WHERE employee_id = {employee_id};"
    )
    major_id = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT location\
              FROM USER\
              WHERE uniqueID = {uniqueID};"
    )
    location = cursor.fetchone()[0]
    cursor.execute(
        f"SELECT first_name, last_name, uniqueID, COUNT(*) AS num\
                FROM USER\
                INNER JOIN COURSE_REGISTRATION\
                ON USER.uniqueID = COURSE_REGISTRATION.student_id\
                WHERE major = '{major_id}' AND location = '{location}'\
                GROUP BY uniqueID\
                HAVING num < 2;"
    )
    students = cursor.fetchall()
    return students


def advisor_home(request):
    cursor = connection.cursor()
    uniqueID = get_uniqueID(request)
    cursor.execute(f"select * from USER where `uniqueID`={uniqueID}")
    user = cursor.fetchone()
    context = {"user": user}

    employee_id = (int)(request.COOKIES.get("uniqueID"))
    uniqueID = request.COOKIES.get("uniqueID")

    students = creditLessThanEight(employee_id, uniqueID, cursor)
    context["creditLessThanEight"] = students

    return render(request, "advisor_home.html", context)


def advisorProfile(request):
    return render(request, "advisor_profile.html")


# list all advisor for the current student
def listAdvisorSql(request):
    if get_user_role(request) != "student":
        return redirect("login")
    cursor = connection.cursor()
    cursor.execute(
        f" select * from "
        f"( select u.uniqueID, u.username, u.first_name, u.last_name, u.role, u.location, u.email, m.major_id, m.major_name, u.phone "
        f"from USER u left join MAJOR m on u.major = m.major_id) t  "
        f'where t.role="advisor" and t.major_id='
        f"(select major from STUDENTS where student_id ={get_uniqueID(request)})"
    )
    rows = cursor.fetchall()
    context = {"data": rows}
    return render(request, "advisorList.html", context)


def listAllCourseSql(request):
    if get_user_role(request) != "student":
        return redirect("login")
    cursor = connection.cursor()
    student_id = get_uniqueID(request)
    # left join and subquery
    cursor.execute(
        f"select * from COURSE a left join "
        f"(select * from COURSE_REGISTRATION where student_id = {student_id}) b "
        f"on a.course_id=b.course_id"
    )
    rows = cursor.fetchall()

    # get credit_limit for student
    cursor.execute(
        f"select credit_limits from STUDENTS where student_id = {student_id}"
    )
    credit_limit = int(cursor.fetchone()[0])

    context = {"data": rows, "credit_limit": credit_limit}
    return render(request, "enrollPage.html", context)


def deleteCourseList(request, courseid):
    uniqueID = request.COOKIES.get("uniqueID")
    if uniqueID is None:
        return redirect("login")
    print(uniqueID)
    print(courseid)
    p = CourseRegistration.objects.filter(student_id=uniqueID, course_id=courseid)
    p.delete()
    return redirect("list")


def register_course(request, course_id):
    cursor = connection.cursor()
    uniqueID = get_uniqueID(request)
    try:

        if request.method == "POST":
            # get total credit for this student
            cursor.execute(
                f"select tg.total from "
                f"(select t.student_id, SUM(credit) total from "
                f"(select cr.course_id, cr.student_id, c.credit from  COURSE_REGISTRATION cr "
                f"left join COURSE c on cr.course_id = c.course_id) t "
                f"group by t.student_id) tg "
                f"where tg.student_id={uniqueID}"
            )
            temp = cursor.fetchone()
            total_credit = 0
            if temp != None:
                total_credit = int(temp[0])

            # get credits for the selected course
            cursor.execute(f"select credit from COURSE where course_id={course_id}")
            curr_course_credit = int(cursor.fetchone()[0])

            # get the credit limits for each student
            cursor.execute(
                f"select credit_limits from STUDENTS where student_id={uniqueID}"
            )
            temp = cursor.fetchone()
            credit_limit = int(temp[0])
            if total_credit + curr_course_credit <= credit_limit:
                cursor.execute(
                    f"INSERT INTO COURSE_REGISTRATION (course_id, student_id) VALUES (%s, %s)",
                    (course_id, uniqueID),
                )
            else:
                print(
                    " \n ****  [ERROR!] exceed credit limit for this semester! contact your advisor if need! *** \n"
                )
            mydb.commit()
        return redirect(listAllCourseSql)
    except:
        # duplicate add
        print(
            "\n *** [ERROR]! The course is already registered, invalid addition! ***\n"
        )
        return redirect(listAllCourseSql)


def adminCourseCreate(request):
    return render(request, "admin_addCourse.html")


def adminCourseAddProcess(request):
    cursor = connection.cursor()
    if request.method == "POST":
        courseName = request.POST["name"]
        proID = request.POST["professor_id"]
        start_date = request.POST["start_date"]
        duration = request.POST["duration"]
        room_id = request.POST["room_id"]
        college_id = request.POST["college_id"]
        credit = request.POST["credit"]
        sql = "INSERT INTO COURSE (name, professor_id, start_date, duration, room_id, college_id, credit) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (courseName, proID, start_date, duration, room_id, college_id, credit)
        cursor.execute(sql, val)
        mydb.commit()
        return redirect(adminCourse)
    else:
        return redirect(adminCourse)


def adminCourseDeleteProcess(request, id):
    cursor = connection.cursor()
    cursor.execute(f"delete from `COURSE_REGISTRATION` where `course_id` = {id}")
    cursor.execute(f"delete from `COURSE` where `course_id` = {id}")
    mydb.commit()
    return redirect(adminCourse)


def adminCourseEdit(request, id):
    cursor = connection.cursor()
    cursor.execute(f"select * from `COURSE` where `course_id` = {id}")
    row = cursor.fetchone()
    context = {"data": row}
    return render(request, "edit.html", context)


def adminCourseUpadate(request, id):
    cursor = connection.cursor()
    if request.method == "POST":
        courseName = request.POST["name"]
        proID = request.POST["professor_id"]
        start_date = request.POST["start_date"]
        duration = request.POST["duration"]
        room_id = request.POST["room_id"]
        college_id = request.POST["college_id"]
        credit = request.POST["credit"]
        cursor.execute(
            """
           UPDATE COURSE
           SET name=%s, professor_id=%s, start_date=%s, duration=%s, room_id=%s, college_id=%s, credit=%s
           WHERE course_id=%s
        """,
            (courseName, proID, start_date, duration, room_id, college_id, credit, id),
        )
        mydb.commit()
        return redirect(adminCourse)
    else:
        return redirect(adminCourse)


def listUserSql(request):
    cursor = connection.cursor()
    cursor.execute("select * from USER")
    rows = cursor.fetchall()
    print(rows)
    context = {"data": rows}
    return render(request, "admin_users.html", context)


def listOneUserSql(request):
    cursor = connection.cursor()
    cursor.execute("select * from USER")
    rows = cursor.fetchone()
    print(rows)
    context = {"data": rows}
    return render(request, "admin_updateUser.html", context)


def adminUserCreate(request):
    return render(request, "admin_addUser.html")


def adminUserAddProcess(request):
    cursor = connection.cursor()
    if request.method == "POST":
        userAccount = request.POST["account"]
        password = request.POST["password"]
        username = request.POST["username"]
        firstName = request.POST["first_name"]
        lastName = request.POST["last_name"]
        role = request.POST["role"]
        location = request.POST["location"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        major = request.POST["major"]
        sql = "INSERT INTO USER (useraccount, password, username, first_name, last_name, role, location, email, phone, login, major) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (
            userAccount,
            password,
            username,
            firstName,
            lastName,
            role,
            location,
            email,
            phone,
            False,
            major,
        )
        cursor.execute(sql, val)
        mydb.commit()
        return redirect(listUserSql)
    else:
        return redirect(listUserSql)


def adminUserEdit(request, id):
    cursor = connection.cursor()
    cursor.execute(f"select * from `USER` where `user_id` = {id}")
    row = cursor.fetchone()
    context = {"data": row}
    return render(request, "admin_updateUser.html", context)


def adminUserUpdate(request, id):
    cursor = connection.cursor()
    if request.method == "POST":
        userAccount = request.POST["account"]
        password = request.POST["password"]
        username = request.POST["username"]
        firstName = request.POST["first_name"]
        lastName = request.POST["last_name"]
        role = request.POST["role"]
        location = request.POST["location"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        cursor.execute(
            """
               UPDATE USER
               SET useraccount=%s, password=%s, username=%s, first_name=%s, last_name=%s, role=%s, location=%s, email=%s, phone=%s
               WHERE user_id=%s
            """,
            (
                userAccount,
                password,
                username,
                firstName,
                lastName,
                role,
                location,
                email,
                phone,
                id,
            ),
        )
        mydb.commit()
        return redirect(listUserSql)
    else:
        return redirect(listUserSql)


def adminUserDeleteProcess(request, id):
    cursor = connection.cursor()
    cursor.execute(f"delete from `USER` where `user_id` = {id}")
    mydb.commit()
    return redirect(listUserSql)


def listOneUserProfile(request):
    cursor = connection.cursor()
    cursor.execute(f"select * from `USER` where `uniqueID`={get_uniqueID(request)}")
    rows = cursor.fetchone()
    context = {"data": rows}
    return render(request, "admin_profile.html", context)


def list_student_profile(request):
    if get_user_role(request) != "student":
        return redirect("login")
    # get logged in Id
    uniqueID = request.COOKIES.get("uniqueID")
    # show the current profile data in the database
    cursor = connection.cursor()
    cursor.execute(f"select * from `USER` where `uniqueID`= {uniqueID}")
    rows = cursor.fetchone()
    context = {"data": rows}
    return render(request, "profilePage.html", context)


def update_student_profile(request):
    # update profile data
    if get_user_role(request) != "student":
        return redirect("login")
    uniqueID = request.COOKIES.get("uniqueID")
    cursor = connection.cursor()
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        location = request.POST["location"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        cursor.execute(
            """
               UPDATE USER
               SET first_name=%s, 
               last_name=%s, 
               location=%s, 
               email=%s, 
               phone=%s
               WHERE uniqueID=%s
            """,
            (first_name, last_name, location, email, phone, uniqueID),
        )
        name = first_name + " " + last_name
        cursor.execute(
            """
           UPDATE STUDENTS
           SET name=%s
           WHERE student_id=%s
        """,
            (name, uniqueID),
        )
        mydb.commit()
        return redirect(list_student_profile)
    else:
        return redirect(list_student_profile)


def list_advisor_profile(request):
    if get_user_role(request) != "advisor":
        return redirect("login")
    cursor = connection.cursor()
    uniqueID = get_uniqueID(request)
    cursor.execute(f"select * from `USER` where uniqueID={uniqueID}")
    rows = cursor.fetchone()
    context = {"data": rows}
    return render(request, "advisor_profile.html", context)


def update_advisor_profile(request):
    # update profile data
    uniqueID = request.COOKIES.get("uniqueID")
    cursor = connection.cursor()
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        location = request.POST["location"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        cursor.execute(
            """
               UPDATE USER
               SET first_name=%s, 
               last_name=%s, 
               location=%s, 
               email=%s, 
               phone=%s
               WHERE uniqueID=%s
            """,
            (first_name, last_name, location, email, phone, uniqueID),
        )
        name = first_name + " " + last_name
        cursor.execute(
            """
           UPDATE ADVISORS
           SET name=%s
           WHERE employee_id=%s
        """,
            (name, uniqueID),
        )
        mydb.commit()
        return redirect(list_advisor_profile)
    else:
        return redirect(list_advisor_profile)


def update_admin_profile(request):
    # update profile data
    uniqueID = request.COOKIES.get("uniqueID")
    cursor = connection.cursor()
    print(request)
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        location = request.POST["location"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        cursor.execute(
            """
               UPDATE USER
               SET first_name=%s, 
               last_name=%s, 
               location=%s, 
               email=%s, 
               phone=%s
               WHERE uniqueID=%s
            """,
            (first_name, last_name, location, email, phone, uniqueID),
        )
        mydb.commit()
        return redirect(adminHome)
    else:
        return redirect(adminHome)
