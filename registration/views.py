from django.shortcuts import render, HttpResponseRedirect
from .forms import UserCreateForm, LoginOtpForm, ForgotPassForm, ResetPassForm, UserProfileForm, \
    AdminProfileForm, StyledAuthenticationForm, StyledPasswordChangeForm # CustomAuthenticationForm
from .utils import send_login_email, send_pass_change_email
from .models import User
from chatapp.forms import GroupForm
from chatapp.models import Group
# from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count


def homepage(request):
    return render(request, 'registration/home.html')


def newregistration(request):
    if request.method == "POST":
        fm = UserCreateForm(request.POST, request.FILES)
        if fm.is_valid():
            email = fm.cleaned_data['email']
            username = fm.cleaned_data['username']
            first_name = fm.cleaned_data['first_name']
            last_name = fm.cleaned_data['last_name']
            password = fm.cleaned_data['password']
            password2 = fm.cleaned_data['password2']
            profile_picture = fm.cleaned_data['profile_picture']
            if len(password) < 8:
                messages.success(request, "password should contain 8 charecters")
                return HttpResponseRedirect('/reg/newreg/')
            if password != password2:
                messages.success(request, "Password and Confirm password does not match...")
                return HttpResponseRedirect('/reg/newreg/')
            User.objects.create_user(email= email, username= username,
                                     first_name= first_name, last_name=last_name, password= password, otp= "",
                                    profile_picture= profile_picture)
            send_login_email(email)
            return HttpResponseRedirect('/reg/otpveri/')
    else:
        fm = UserCreateForm()
    return render(request,'registration/create.html', {'FORM':fm})



def otpverify(request):
    if request.method == "POST":
        fm = LoginOtpForm(request.POST)
        if fm.is_valid():
            otp = fm.cleaned_data['otp']
            email = fm.cleaned_data['email']
            user = User.objects.filter(email= email).exists()
            if user == True:
                user = User.objects.get(email= email)
                if user.otp == otp:
                    user.is_verified = True
                    user.save()
                    return HttpResponseRedirect('/reg/login/')
                else:
                    messages.success(request, "Wrong OTP")
            else:
                messages.success(request, "Sorry... No user present with this credential")
    else:
        fm = LoginOtpForm()
    return render(request, 'registration/otp.html', {'FORM':fm})



def userlogin(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = StyledAuthenticationForm(request= request, data= request.POST)
            # fm = CustomAuthenticationForm(request= request, data= request.POST)
            if fm.is_valid():
                # print('ok')
                uemail = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username= uemail, password= upass)
                if user is not None:
                    if user.is_verified == False:
                        messages.success(request, "You are not verified...")
                        return HttpResponseRedirect('/reg/login/')
                    login(request, user)
                    return HttpResponseRedirect('/reg/profile/')
                else:
                    fm = StyledAuthenticationForm()
                    messages.success(request, "You are not a user")
                    return render(request, 'registration/loginpage.html', {'FORM':fm})
        else:
            fm = StyledAuthenticationForm()
            # fm = CustomAuthenticationForm()
        return render(request, 'registration/loginpage.html', {'FORM':fm})
    else:
        return HttpResponseRedirect('/reg/profile/')



@login_required
def userprofile(request):
    if request.user.is_authenticated:
        all_user = User.objects.all()
        # all_groups = Group.objects.filter(members=request.user).annotate(
        #                                     num_members=Count('members')).filter(num_members__gt=3)
        all_groups = Group.objects.filter(members=request.user).annotate(
                                            num_members=Count('members')).filter(members__gt=3)
        if request.method == "POST":
            if request.user.is_admin == True:
                fm = AdminProfileForm(request.POST, instance= request.user)
                user = all_user
            else:
                fm = UserProfileForm(request.POST, instance= request.user)
                user = None
            if fm.is_valid():
               fm.save()
               messages.success(request, "Your Profile data is updated")
        else:
            if request.user.is_admin == True:
                fm = AdminProfileForm(instance= request.user)
                user = all_user
            else:
                fm = UserProfileForm(instance= request.user)
                user = None
        return render(request, 'registration/profilepage.html', {'nm': request.user, 'FORM': fm, 'users':user, 
                                                                 'chat_users':all_user.exclude(email=request.user),
                                                                 'all_groups':all_groups})
    else:
        return HttpResponseRedirect('/reg/login/')




@login_required
def userchangepass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = StyledPasswordChangeForm(user= request.user, data= request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, "Your password has been changed")
                return HttpResponseRedirect('/reg/login/')
            else:
                messages.success(request, "Re-write your password")
                return HttpResponseRedirect('/reg/chpass/')
        else:
            fm = StyledPasswordChangeForm(user= request.user)
            return render(request, 'registration/changepass.html', {'FORM':fm})
    else:
        return HttpResponseRedirect('/reg/login/')
    



def userforgotpass(request):
    if request.method == 'POST':
        fm = ForgotPassForm(request.POST)
        if fm.is_valid():
            email = fm.cleaned_data['email']
            user = User.objects.filter(email= email).exists()
            if user == True:
                user = User.objects.get(email= email)
                send_pass_change_email(user.email)
                user.is_verified = False
                return HttpResponseRedirect('/reg/resetpass/')
            else:
                fm = ForgotPassForm()
                messages.success(request, "no user present")
                return render(request, 'registration/forgotpass.html', {'FORM':fm})
        else:
            fm = ForgotPassForm()
            messages.success(request, "Form not valid")
            return render(request, 'registration/forgotpass.html', {'FORM':fm})
    else:
        fm = ForgotPassForm()
        return render(request, 'registration/forgotpass.html', {'FORM':fm})
    


def userresetpass(request):
    if request.method == 'POST':
        fm = ResetPassForm(request.POST)
        if fm.is_valid():
            email = fm.cleaned_data['email']
            otp = fm.cleaned_data['otp']
            password1 = fm.cleaned_data['password1']
            password2 = fm.cleaned_data['password2']
            user = User.objects.filter(email= email).exists()
            if user == True:
                user = User.objects.get(email= email)
                if user.otp == otp:
                    if len(password1) < 8:
                        messages.success(request, "password should contain 8 charecters")
                        return HttpResponseRedirect('/reg/resetpass/')
                    if password1 != password2:
                        messages.success(request, "Password and Confirm password does not match...")
                        return HttpResponseRedirect('/reg/resetpass/')
                    user.set_password(password1)
                    user.is_verified = True
                    user.save()
                    return HttpResponseRedirect('/reg/login/')
                else:
                    fm = ResetPassForm()
                    messages.success(request, 'OTP does not match')
                    return render(request, 'registration/resetpassword.html', {'FORM':fm})
            else:
                fm = ResetPassForm()
                messages.success(request, 'No user found')
                return render(request, 'registration/resetpassword.html', {'FORM':fm})
        else:
            fm = ResetPassForm()
            messages.success(request, 'Form not valid')
            return render(request, 'registration/resetpassword.html', {'FORM':fm})
    else:
        fm = ResetPassForm()
        messages.success(request, 'Wrong request')
        return render(request, 'registration/resetpassword.html', {'FORM':fm})
    

@login_required
def userdetailpage(request, pk):
    if request.user.is_authenticated:
        if request.method == "GET":      ## "POST"
            if request.user.is_admin == True:
                user = User.objects.get(pk = pk)
                fm = AdminProfileForm(instance= user)
            else:
                fm = AdminProfileForm(instance= request.user)
        else:
            fm = AdminProfileForm(instance= request.user)
        return render(request, 'registration/userdetail.html', {'FORM':fm})
    else:
        return HttpResponseRedirect('/reg/login/')
    


def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/reg/login/')
