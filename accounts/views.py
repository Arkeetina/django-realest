from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

from contacts.models import Contact



# Create your views here.
def register(req):
    if req.method == 'POST':
        # messages.error(req, 'Testing error message')
        first_name = req.POST['first_name']
        last_name = req.POST['last_name']
        username = req.POST['username']
        email = req.POST['email']
        password = req.POST['password']
        password2 = req.POST['password2']
        # Check if password match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(req, 'This username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(req, 'This email is taken')
                    return redirect('register')
                else:
                    # looks good
                    user = User.objects.create_user(username=username, password=password, email=email,
                    first_name=first_name, last_name=last_name)
                    # login after register
                    #auth.login(req, user)
                    #messages.success(req, 'You are now logged in')
                    # return redirect('index')
                    user.save()
                    messages.success(req, 'You are now registered and can log in')
                    return redirect('login')
        else:
            messages.error(req, 'Passwords do not match')
            return redirect('register')
    else:
        return render(req, 'accounts/register.html')

def login(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(req, user)
            messages.success(req, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(req, 'Invalid credentials')
            return redirect('login')
    else:
        return render(req, 'accounts/login.html')

def logout(req):
    if req.method == 'POST':
        auth.logout(req)
        messages.success(req, 'You are now logged out')
        return redirect('index')

def dashboard(req):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=req.user.id)
    context = {
        'contacts': user_contacts
    }
    return render(req, 'accounts/dashboard.html', context)

