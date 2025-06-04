
from django.contrib import admin
from django.urls import path, include
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', 
         CreateView.as_view(
             template_name='registration/register.html',
             form_class=CustomUserCreationForm,
             success_url=reverse_lazy('login')
         ), 
         name='register'),
    
    path('', HomeView.as_view(), name='home'),
    path('pacientes/', include('pacientes.urls')),
    path('servicos/', include('servicos.urls')),
]
