from django.shortcuts import render,redirect
from django.views.generic import View
from myapp.models import ToDo
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.cache import never_cache




def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid section")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
desc=[signin_required,never_cache]





class TodoForm(forms.ModelForm):

    class Meta():
       model=ToDo
       exclude=("created_date","user_object")



class SignUpForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]



class LoginForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))



@method_decorator(desc,name="dispatch")
class TodoListView(View):

    def get(self,request,*args,**kwargs):
        qs=ToDo.objects.filter(user_object=request.user)
        return render(request,"todo_list.html",{"data":qs})
    

    
@method_decorator(desc,name="dispatch")
class TodoCreateView(View):

    def get(self,request,*args,**kwargs):
        form=TodoForm()
        return render(request,"todo_create.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=TodoForm(request.POST)
        
        if form.is_valid():
            data=form.cleaned_data
            ToDo.objects.create(**data,user_object=request.user)
            messages.success(request,"todo added successfully")
            return redirect("todo-list")
        else:
            messages.error(request,"todo adding failed")
            return render(request,"todo_create.html",{"form":form})
        




@method_decorator(desc,name="dispatch")
class ToDoDetailView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=ToDo.objects.get(id=id)
        return render(request,"todo_detail.html",{"data":qs})
    


@method_decorator(desc,name="dispatch")
class ToDoDeleteView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        ToDo.objects.filter(id=id).delete()
        return redirect("todo-list")
    


@method_decorator(desc,name="dispatch")
class ToDoUpdateView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=ToDo.objects.get(id=id)       
        form=TodoForm(instance=todo_object)
        return render(request,"todo_update.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_objects=ToDo.objects.get(id=id)
        form=TodoForm(request.POST,instance=todo_objects)
        if form.is_valid():
            form.save()
            return redirect("todo-list")
        else:
            return render(request,"todo_update.html",{"form":form})
        





class SignupView(View):
    def get(self,request,*args,**kwargs):
        form=SignUpForm()
        return render(request,"registration.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=SignUpForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            print("account added")
            return redirect("signin")
        else:
            return render(request,"registration.html",{"form":form})
       



           
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render (request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                login(request,user_object)
                return redirect ("todo-list")
        return render(request,"login.html",{"form":form})
    



@method_decorator(desc,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
