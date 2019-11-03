from django.http import HttpResponseRedirect
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

    def form_valid(self, form, **kwargs):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ('first_name', 'last_name', 'birthdate', 'email',
              'website', 'country', 'city', 'year', 'picture')
    success_url = reverse_lazy('profile_changelist')


def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'profiles/city_dropdown_list_options.html', {'cities': cities})
