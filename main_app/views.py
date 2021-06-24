from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
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






########### user data
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

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/cats')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            u = form.cleaned_data['username']
            login(request, user)
            return redirect('/user/' + str(user))
        else:
            print('<h1>Invalid combination user and password<h1>')
            return redirect('/signup')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    cats = Cat.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'cats': cats})



####### Cats data
@method_decorator(login_required, name='dispatch')
class CatCreate(CreateView):
  model = Cat
  fields = ['name', 'breed', 'description', 'age', 'cattoys']
  #   if creating is sucesffful return to /cat
#   success_url = '/cats'

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.user = self.request.user
    self.object.save()
    return HttpResponseRedirect('/cats')
    # return HttpResponseRedirect('/cats/' + str(self.object.pk))


class CatUpdate(UpdateView):
  model = Cat
  fields = ['name', 'breed', 'description', 'age', 'cattoys']


  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.save()
    return HttpResponseRedirect('/cats/' + str(self.object.pk))



class CatDelete(DeleteView):
  model = Cat
  success_url = '/cats'


def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {'cats': cats})


def cats_show(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    data = { 'cat': cat }
    return render(request, 'cats/show.html', data)






#####cat toys
def cattoys_index(request):
    cattoys = CatToy.objects.all()
    return render(request, 'cattoys/index.html', {'cattoys': cattoys})



def cattoys_show(request, cattoy_id):
    cattoy = CatToy.objects.get(id=cattoy_id)
    return render(request, 'cattoys/show.html', {'cattoy': cattoy})



class CatToyCreate(CreateView):
    model = CatToy
    fields = '__all__'
    success_url = '/cattoys'


class CatToyUpdate(UpdateView):
    model = CatToy
    fields = ['name', 'color']
    success_url = '/cattoys'

class CatToyDelete(DeleteView):
    model = CatToy
    success_url = '/cattoys'



def assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).cattoys.add(toy_id)
    #return HttpResponseRedirect('/cats/'+str(cat_id))
    return redirect('cats_show', cat_id=cat_id) ## Alternative wat of doing redirect

def unassoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).cattoys.remove(toy_id)
    return HttpResponseRedirect('/cats/'+str(cat_id))







###### default view
def about(request):
    return render(request, 'about.html')
    
def index(request):
    return render(request, 'index.html')

























# main_app/views.py



