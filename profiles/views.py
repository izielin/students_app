from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
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
    success_url = reverse_lazy('profile')

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('profile', kwargs={'pk': pk})

    def get(self, request, *args, **kwargs):
        if not request.user.id == self.kwargs.get('pk'):
            raise Http404
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.id == self.kwargs.get('pk'):
            raise Http404
        return super().post(request, *args, **kwargs)


def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'profiles/city_dropdown_list_options.html', {'cities': cities})


@login_required
def profile(request, pk):
    profile_data = Profile.objects.get(user=pk)
    context = {
        'profile': profile_data,
    }
    if Profile.objects.filter(user=request.user.id).count() == 1:
        return render(request, 'profiles/profile.html', context)
    else:
        return HttpResponseRedirect('add')