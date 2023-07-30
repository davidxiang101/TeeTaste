from django.contrib import admin
from .models import Shoe
from .models import User

admin.site.register(Shoe)

admin.site.register(User)