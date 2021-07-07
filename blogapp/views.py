from django.shortcuts import redirect, render,HttpResponseRedirect
from .forms import SignUpForm,LogInForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post,Contact,Profile
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings
import uuid

#For Email Sending.
def email_sender(email,token,username):
    subject = 'Verify Email'
    message = f'''
      Hello , {username}
          You registered an account on GitHub Image Fetcher WebSite, before being able to use you account you need to verify that this is your email address by clicking here: http://127.0.0.1:8000/account_verify/{token}/
                  
          Kind Regards,Team Goyanka'''
    #Click On the Link to verify your account http://127.0.0.1:8000/account_verify/{token}/
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail(subject, message, email_from, recipient_list)

#For Account Varification.
def account_verify(request,token):
    profile=Profile.objects.filter(token=token).first()
    profile.verify=True
    profile.save()
    messages.success(request,"Your account has been varified , You can LogIn Now")
    return HttpResponseRedirect('/login/')

# This is HomePage View. 
def home(request):
    posts=Post.objects.all()
    return render(request,'home.html',{'posts':posts})

# This is AboutPage View.
def about(request):
    return render(request,'about.html')

# This is Contact Page View.
def contact(request):
    if request.method == "POST":
      user_name=request.POST['name']
      user_email=request.POST['email']
      user_add=request.POST['address'] 
      user_msg=request.POST['msg']
      contact=Contact(name=user_name,email=user_email,address=user_add,message=user_msg)
      contact.save()
      messages.success(request,"We Will Contact You Soon !!")
      return redirect('/contact/')
    else:
      return render(request,'contact.html')   







# This is Dashboard Page View.
def dashboard(request):
    if request.user.is_authenticated:
      posts=Post.objects.all()
      user=request.user
      full_name=user.get_full_name()
      gps=user.groups.all()
      return render(request,'dashboard.html',{'posts':posts,'name':full_name,'groups':gps})
    else :
      return HttpResponseRedirect('/login/')  

# This is User Logout View.
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# This is User Login View.
def user_login(request):
  if not request.user.is_authenticated:
     if request.method == "POST":
         form=LogInForm(request=request,data=request.POST)
         if form.is_valid():
           uname =form.cleaned_data['username']
           upass =form.cleaned_data['password']
           user =authenticate(username=uname,password=upass)
           if user is not None:
            profile=Profile.objects.filter(user=user).first()           
            if profile.verify:
              login(request, user)
              return HttpResponseRedirect('/dashboard/')
            messages.info(request,"You are not varified , Check Your Gmail Account and varify yourself !")
            return HttpResponseRedirect("/login/")
     else:
      form=LogInForm()
     return render(request,'login.html',{'form':form})
  else:
       return user_logout(request)

# This is User SignUp View.
def user_signup(request):
  if not request.user.is_authenticated:
    if request.method == "POST":
       form=SignUpForm(request.POST)
       if form.is_valid():
           user=form.save() 
           group=Group.objects.get(name="Author")
           user.groups.add(group)    
           uid=uuid.uuid4()
           profile=Profile(user=user,token=uid)
           profile.save()
           email_sender(user.email,uid,user.username) 
           messages.success(request,"Your Account Created Successfully , to Varify your Account Check Your Email !")
           return redirect('/signup/')
    else :
       form=SignUpForm() 
    return render(request,'signup.html',{'form':form})
  else:
      return user_logout(request)


# This is AddPost View.
def add_post(request):
     if request.user.is_authenticated:
        if request.method == "POST":
            form=PostForm(request.POST)
            if form.is_valid():
                form.save()
        form=PostForm()
        return render(request,'addpost.html',{'form':form})
     else:
         HttpResponseRedirect('/login/') 





# This is Update Page View.
def update_post(request,id):
     if request.user.is_authenticated:
       if request.method=="POST":
           pi=Post.objects.get(pk=id)
           form=PostForm(request.POST,instance=pi)
           if form.is_valid():
               form.save()   
       else:
           pi=Post.objects.get(pk=id)             
           form=PostForm(instance=pi)
       return render(request,'updatepost.html',{'form':form,'id':id})
     else:
         HttpResponseRedirect('/login/') 

# This is Delete View.
def delete_post(request,id):
     if request.user.is_authenticated:
        if request.method=="POST":
            pi=Post.objects.get(pk=id)
            pi.delete()  
            return HttpResponseRedirect("/dashboard/")
     else:
         HttpResponseRedirect('/login/') 