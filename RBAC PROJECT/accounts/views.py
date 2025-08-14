from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from accounts.models import CustomUser, Student


# Create your views here.
@login_required
def home(request):
    return render(request,'home.html')


def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password = request.POST.get('password')

        user=authenticate('request',username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'username and password not matched')

            return redirect('login')
    return render(request,'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Username already exists. Please try another.')

                return render(request,'registration.html')
            else:
                user = CustomUser.objects.create(username=username,
                                                 email=email,
                                                 password=make_password(password1),
                                                 role='admin')
                return redirect('login')


        else:
            messages.error('password not matched')
    return render(request,'registration.html')

from django.contrib.auth import logout as auth_logout
def logout(request):
    auth_logout(request)
    return redirect('login')


def employee_list(request):
    employees=CustomUser.objects.all().values()
    return render(request,'employee_list.html',{'employees':employees})


def student_list(request):
    #student_data=Student.objects.all().values()
    user = request.user
    if user.role == 'admin':
       student_data = Student.objects.select_related('added_by').all()
    else:
        student_data = Student.objects.select_related('added_by').all().filter(added_by=user)

    return render(request,'student_list.html',{'student_data':student_data})


def add_new_student(request):
    if request.method == "POST":
        if request.user.role == 'admin':
            added_by_id = request.POST.get("added_by")
            added_by=CustomUser.objects.get(id=added_by_id)
        else:
            added_by = request.user
        coordinator= request.POST.get('coordinator')
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        place = request.POST.get('place')
        gender = request.POST.get('gender')
        skillset_list = request.POST.getlist('skillset')
        skillset=",".join(skillset_list)
        state = request.POST.get('state')
        # 💥 Check if email already exists
        if Student.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different one.")
            users = CustomUser.objects.all() if request.user.role == 'admin' else [request.user]
            return render(request, 'add_student.html', {
                "users": users,
                # "skills": skillset_list,
                # "student": {
                #     "name": name, "email": email, "age": age,
                #     "place": place, "gender": gender, "state": state
             #   }
            })

        Student.objects.create(added_by=added_by,name=name, email=email,
                               age=age, place=place, gender=gender,
                               skillset=skillset, state=state)
    user = CustomUser.objects.all() if request.user.role == "admin" else [request.user]
    return render(request,'add_student.html',{'users':user})


def update_student(request,id):
    student = get_object_or_404(Student,id=id)
    users = CustomUser.objects.all()
    if request.method == 'POST':
        email = request.POST.get('email')
        if Student.objects.exclude(id=id).filter(email=email).exists():
            return render(request,'add_student.html',{'users':users,
                                                                            'student':student})
        student.name = request.POST.get('name')
        student.email = request.POST.get('email')
        student.age = request.POST.get('age')
        student.place = request.POST.get('place')
        student.gender = request.POST.get('gender')
        skillset_list = request.POST.getlist('skillset')
        student.skillset = ",".join(skillset_list)
        student.state = request.POST.get('state')
        added_by_id = request.POST.get("added_by")
        student.added_by = CustomUser.objects.get(id=added_by_id)
        student.save()
        return redirect('student_list.html')
    return render(request,'add_student.html',{'users':users,'student':student})



def delete_student(request,id):
    student_data=Student.objects.get(id=id)
    student_data.delete()
    return HttpResponse("welcome to delete")