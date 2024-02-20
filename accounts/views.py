from django.shortcuts import render,HttpResponse,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

# varification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

#normal user ke use kiya create_user dusra super user k liye
            user = Account.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = password,
                username = username
            )
            user.phone_number = phone_number                              #y variable model me nhi bnaya toh yaha define kr diya

            user.save()

            # account activation
            current_site = get_current_site(request)
            mail_subject = 'please Activate Your Account'
            message = render_to_string('account/account_varification_mail.html' ,{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.id)),
                'token':default_token_generator.make_token(user)

            })

            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()




            # error message for not matching  passwords
            messages.success(request, 'Registration successfull...')
            return redirect('register')
    else:
        form = RegistrationForm()
    context = {
        'form':form
    }
    return render(request,'account/register.html',context)


#use active user for login which is you register the first in django administration
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are now logged in!')
            return redirect('home')
        else:
            messages.error(request, 'invalid credentials')
            return redirect('login')
    return render(request, 'account/login.html')


#logout
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'you are logged out')
    return redirect('login')


def activate(request,uidb,token):
    return HttpResponse('ok')
