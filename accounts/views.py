from django.views.generic import CreateView
from accounts.forms import RegistrationForm

# Create your views here.

class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "register.html"
    success_url = '/login'