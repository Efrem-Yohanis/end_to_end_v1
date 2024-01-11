from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired redirect URL after successful login
        else:
            # Handle invalid credentials error
            messages.error(request,'Invalid credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):
    all_user = CustomUser.objects.all()
    context = {'all_user': all_user}
    return render(request, 'Home.html', context)


def registration(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        address = request.POST['address']
        role = request.POST['role']
        date_of_birth = request.POST['date_of_birth']
        
        if not re.match("^[a-zA-Z]*$", first_name):
            messages.error(request, 'First name should only contain letters')
            return render(request, 'Registration.html', {})
        elif not re.match("^[a-zA-Z]*$", last_name):
            messages.error(request, 'Last name should only contain letters')
            return render(request, 'Registration.html', {})
        elif not re.match("^[a-zA-Z]*$", username):
            messages.error(request, 'Username should only contain letters')
            return render(request, 'Registration.html', {})
        elif not re.match(r'^\+[0-9]{1,3}\s?[0-9]{9,15}$', phone):
            messages.error(request, 'Phone number should be in the format +1234567890')
            return render(request, 'Registration.html', {})
        elif password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return render(request, 'Registration.html', {})
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return render(request, 'Registration.html', {})
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                
                # Create your CustomUser object here
                newuser = CustomUser.objects.create(user=user,email=email, first_name=first_name, date_of_birth=date_of_birth, role=role, address=address, phone=phone, username=username, last_name=last_name)
                
                if newuser:
                    messages.success(request, 'User successfully created. Please login using username and password.')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
    
    return render(request, 'Registration.html', {})




@login_required
def update(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    context = {'user': user}

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        role = request.POST['role']
        date_of_birth = request.POST['date_of_birth']

        if not first_name.isalpha():
            messages.error(request, 'First name can only contain letters.')
        elif not last_name.isalpha():
            messages.error(request, 'Last name can only contain letters.')
        elif not username.isalpha():
            messages.error(request, 'Username can only contain letters.')
        elif not re.match(r'^\(\d{3}\)\s\d{3}-\d{4}$', phone):
            messages.error(request, 'Phone number must be in the format: (123) 456-7890.')
        else:
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.phone = phone
            user.address = address
            user.role = role

            birth_date = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d").date()
            today = datetime.date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

            if age < 20:
                messages.error(request, 'Age must be above 20 years.')
            else:
                user.date_of_birth = date_of_birth
                user.save()
                messages.success(request, 'User information updated successfully.')
                return redirect('home')

    return render(request, 'update.html', context)


@login_required
def view_detail(request,user_id):
    user=CustomUser.objects.get(id=user_id)
    context={'user':user}
    return render(request,'view_detail.html',context)


@login_required
def delete(request, user_id):
    user=request.user
    req_user=CustomUser.objects.get(user=user)

    if req_user.role == 'User':
         messages.error(request, 'Sorry This action is not allowed for you! only be done by the administrator.')

    else:
        get_user=CustomUser.objects.get(id=user_id)
        if(user==get_user.user):
            messages.error(request, 'You cannot delete your own account.')
        
        else:
            user1=get_user.user
            user_to_delete = get_object_or_404(User, id=user1.id)
            user_to_delete.delete()
            messages.success(request, 'User deleted successfully.')
   

    return redirect('home')  # Redirect to the home page regardless of the deletion attempt