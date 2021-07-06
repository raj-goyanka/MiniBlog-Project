from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm,LogInForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group

# This is HomePage View. 
def home(request):
    posts=Post.objects.all()
    return render(request,'home.html',{'posts':posts})

# This is AboutPage View.
def about(request):
    return render(request,'about.html')

# This is Contact Page View.
def contact(request):
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
              login(request,user)  
              messages.success(request,"User Logged  in Successfully!!")
              return HttpResponseRedirect("/dashboard/")
     else:
      form=LogInForm()
     return render(request,'login.html',{'form':form})
  else:
       return HttpResponseRedirect("/dashboard/")

# This is User SignUp View.
def user_signup(request):
    if request.method == "POST":
       form=SignUpForm(request.POST)
       if form.is_valid():
           messages.success(request,"Congratulation!!!You have become a Author. ")
           user=form.save() 
           group=Group.objects.get(name="Author")
           user.groups.add(group)     
    else :
       form=SignUpForm() 
    return render(request,'signup.html',{'form':form})

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