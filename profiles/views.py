from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Profile, City
from .forms import ProfileForm


class ProfileListView(ListView):
    model = Profile
    context_object_name = 'profiles'


class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('profile_changelist')


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('profile_changelist')


def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'profiles/city_dropdown_list_options.html', {'cities': cities})
