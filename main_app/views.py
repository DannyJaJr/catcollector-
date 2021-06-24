from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import render, redirect
from .models import Cat

# import the CatToy model
from .models import Cat, CatToy

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/cats')

def login_view(request):
     # if post, then authenticate (user submitted username and password)
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/'+u)
                else:
                    print('The account has been disabled.')
                    return HttpResponseRedirect('/login')
            else:
                print('The username and/or password is incorrect.')
                return HttpResponseRedirect('/login')
    else: # it was a get request so send the emtpy login form
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            u = form.cleaned_data['username']
            login(request, user)
            return redirect('/cats')
        else:
            print('Invalid combination user and password')
            return redirect('/signup')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


def cattoys_index(request):
    cattoys = CatToy.objects.all()
    return render(request, 'cattoys/index.html', {'cattoys': cattoys})

def cattoys_show(request, cattoy_id):
    cattoy = CatToy.objects.get(id=cattoy_id)
    return render(request, 'cattoys/show.html', {'cattoy': cattoy})



# Create your views here.
def about(request):
    return render(request, 'about.html')
    
def index(request):
    return render(request, 'index.html')





@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    cats = Cat.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'cats': cats})




def cats_index(request):
    cats = Cat.objects.all()
    data = {
        'cats': cats
    }
    return render(request, 'cats/index.html', data)


def cats_show(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    data = { 'cat': cat }
    return render(request, 'cats/show.html', data)





class CatToyUpdate(UpdateView):
    model = CatToy
    fields = ['name', 'color']
    success_url = '/cattoys'

class CatToyDelete(DeleteView):
    model = CatToy
    success_url = '/cattoys'



# main_app/views.py
class CatCreate(CreateView):
  model = Cat
  fields = ['name', 'breed', 'description', 'age', 'cattoys']
  #   if creating is sucesffful return to /cat
#   success_url = '/cats'

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.user = self.request.user
    self.object.save()
    return HttpResponseRedirect('/cats/' + str(self.object.pk))

class CatUpdate(UpdateView):
  model = Cat
  fields = ['name', 'breed', 'description', 'age', 'cattoys']
#   fields = ['name', 'breed', 'description', 'age']

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.save()
    return HttpResponseRedirect('/cats/' + str(self.object.pk))

@method_decorator(login_required, name='dispatch')
class CatDelete(DeleteView):
  model = Cat
  success_url = '/cats'

class CatToyCreate(CreateView):
    model = CatToy
    fields = '__all__'
    success_url = '/cattoys'