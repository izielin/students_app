from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Profile, City
from .forms import ProfileForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def profiles_list(request):
    profile_list = Profile.objects.all()
    query = request.GET.get('q')
    if query:
        profile_list = Profile.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).distinct()

    paginator = Paginator(profile_list, 15)  # 15 profiles per page
    page = request.GET.get('page')

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    context = {
        'profiles': profiles
    }
    return render(request, "profiles/studentprofile_list.html", context)


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_student:
            self.fields = ('first_name', 'last_name', 'birthdate',
                      'website', 'country', 'city', 'year', 'picture')
        else:
            self.fields = ['first_name', 'last_name', 'birthdate',
                      'website', 'country', 'city', 'picture']
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form, **kwargs):
        form.instance.email = self.request.user.email
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('profile', kwargs={'pk': pk})

    def get(self, request, *args, **kwargs):
        if request.user.id != self.kwargs.get('pk'):
            print(request.user.id, self.kwargs.get('pk'))
            raise Http404
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.id == self.kwargs.get('pk'):
            raise Http404
        return super().post(request, *args, **kwargs)

    def test_func(self):
        return True

def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'profiles/city_dropdown_list_options.html', {'cities': cities})


@login_required
def profile(request, pk):
    profile_data = Profile.objects.get(user=request.user)
    context = {
        'profile': profile_data,
    }
    return render(request, 'profiles/profile.html', context)
