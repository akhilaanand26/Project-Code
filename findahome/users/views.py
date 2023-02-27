from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm,SignupForm
from .helpers import send_forget_password_email
from .models import Profile ,User
from .constants import TENANT
import uuid



def login_view(request):

    if ((request.user.is_authenticated)):
        return redirect('properties:home')
    
    common_error = ""

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

           
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
               
                if user.role == TENANT:
                    return redirect('properties:home')
                else:
                    return redirect('owner:properties')


            else:
                
               common_error = "Invalid email or password"
    else:
        form = LoginForm()

    return render(request, "users/login.html", {'form': form, "common_error": common_error})

def signup_view(request):
    
    if ((request.user.is_authenticated)):
        return redirect('properties:home')
    
    if request.method == "POST":
        form = SignupForm(request.POST)

        
        if form.is_valid():
           
            user_obj =  form.save()

            profile_obj = Profile.objects.create(user = user_obj)
            profile_obj.save()

            messages.success(request, "Your account has been created successfully, please login to continue")
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, "users/signup.html", { "form": form })

def logout_view(request):
    logout(request)
    return redirect("properties:home")

def ChangePassword(request,token):
    context = {}
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        context = {'user_id':profile_obj.user.id}
       
        if request.method == 'POST':
            new_password= request.POST.get('new_password')
            print(new_password)
            confirm_password=request.POST.get('reconfirm_password')
            user_id=profile_obj.user.id

        if user_id is None:
            message.success(request,'No user id found')
            return redirect(f'/change-password/{token}/')


        if new_password!= confirm_password:
            message.success(request,'Both shoud be equal.')
            return redirect(f'/change-password/{token}/')


        user_obj= User.objects.get(id = user_id)
        user_obj.set_password(new_password)
        user_obj.save()  
        return redirect('login')  


        print(profile_obj)
       
    except Exception as e:
        print(e)
    return render(request,'users/change-password.html',context)




def forgetpswd(request):
    try:
        if request.method=='POST':
            email=request.POST.get('email')
            

            if not User.objects.filter(email=email).first():
                messages.success(request,'No user found with this email.')
                return redirect('/forgetpswd/')

            user_obj = User.objects.get(email=email)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
           
            send_forget_password_email(user_obj.email , token)
            messages.success(request,'An email is send.')
            return redirect('/forgetpswd/')


    except Exception as e:
        print(e)
    return render(request,'users/forgetpswd.html')    

   