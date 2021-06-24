from django.contrib import admin

# Register your models here.
from .models import Cat
from .models import Cat, CatToy




# Register the models here
admin.site.register(Cat)
admin.site.register(CatToy)