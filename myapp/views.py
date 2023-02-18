from django.shortcuts import render, redirect
from .models import Contact, User
from django.conf import settings
from django.core.mail import send_mail
import random
# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        try:
            print(request.POST['email'])
            user = User.objects.get(email=request.POST['email'])
            if user.password == request.POST['password']:
                request.session['email'] = user.email
                request.session['profile_pic'] = user.profile_pic.url
                request.session['fname'] = user.fname
                return render(request, 'index.html')
            else:
                msg = "Incorrect Email"
                return render(request, 'login.html', {'msg': msg})

        except:
            msg = "Email Not Registered"
            return render(request, 'login.html', {'msg': msg})
    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == "POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg = "Email Already Register"
            return render(request, 'signup.html', {'msg': msg})

        except:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    location=request.POST['location'],
                    gender=request.POST['gender'],
                    password=request.POST['password'],
                    remarks=request.POST['remarks'],
                    profile_pic=request.FILES['profile_pic'],
                )
                msg = "User Sign Up Successfully"
                return render(request, 'signup.html', {'msg': msg})
            else:
                msg = "Password & Confirm Password does not Matched"
                return render(request, 'signup.html', {'msg': msg})

    else:
        return render(request, 'signup.html')


def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST['name'],
            mobile=request.POST['mobile'],
            email=request.POST['email'],
            gender=request.POST['gender'],
            remarks=request.POST['remarks']
        )
        contacts = Contact.objects.all().order_by("-id")[:5]
        msg = "Contact Saved Successfully"
        return render(request, 'contact.html', {'msg': msg}, {'contacts': contacts})

    else:
        contacts = Contact.objects.all().order_by("-id")[:5]

        return render(request, 'contact.html', {'contacts': contacts})


def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        del request.session['profile_pic']
        return render(request, 'login.html')
    except:
        return render(request, 'login.html')


def forgot_password(request):
    if request.method == "POST":
        try:
            otp = random.randint(1000, 9999)
            user = User.objects.get(email=request.POST['email'])
            subject = 'OTP for Forgot Password'
            message = 'OTP for Forgot Password is'+" "+str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            return render(request, 'otp.html', {'otp': otp, 'email': user.email})
        except:
            return render(request, 'forgot-password.html')

    else:
        return render(request, 'forgot-password.html')


def verify_otp(request):
    Email = request.POST['email']
    Otp = request.POST['otp']
    Uotp = request.POST['uotp']
    if Otp == Uotp:
        return render(request, 'new-password.html', {'email': Email})
    else:
        msg = "Invalid OTP"
        return render(request, 'otp.html', {'otp': Otp, 'email': Email, 'msg': msg})


def new_password(request):
    email = request.POST['email']
    np = request.POST['new-password']
    cnp = request.POST['cnew-password']
    if np == cnp:
        user = User.objects.get(email=email)
        user.password = np
        user.save()
        msg = "Password Updated Successfully"
        return render(request, 'login.html', {'msg': msg})
    else:
        msg = "New Password & Confrim Password does not Matched"
        return render(request, 'login.html', {'msg': msg})


def change_password(request):
    if request.method == "POST":
        old_password = request.POST['old-password']
        new_password = request.POST['new-password']
        cnew_password = request.POST['cnew-password']
        try:
            user = User.objects.get(email=request.session['email'])
            if user.password == old_password:
                if new_password == cnew_password:
                    user.password = new_password
                    user.save()
                    return redirect('logout')
                else:
                    msg = "New Password & Confrim New Password does not Matched"
                    return render(request, 'change-password.html', {'msg': msg})
            else:
                msg = "Old Password & New Password does not Matched"
                return render(request, 'change-password.html', {'msg': msg})
        except:
            msg = "Please Login First"
            return render(request, 'login.html', {'msg': msg})
    else:
        return render(request, 'change-password.html')


def profile(request):
    user = User.objects.get(email=request.session['email'])
    if request.method == "POST":
        user.fname = request.POST['fname']
        user.lname = request.POST['lname']
        user.location = request.POST['location']
        user.gender = request.POST['gender']
        user.mobile = request.POST['mobile']
        user.remarks = request.POST['remarks']
        try:
            user.profile_pic = request.FILES['profile_pic']
        except:
            pass
        msg = "Profile Update Successfully"
        user.save()
        request.session['profile_pic'] = user.profile_pic.url
        request.session['fname']=user.fname
        return render(request, 'profile.html', {'user': user, 'msg': msg})
    else:
        return render(request, 'profile.html', {'user': user})
