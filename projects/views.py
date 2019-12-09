from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView
from .forms import ProjectForm, MarkForm, CourseForm
from .models import Project, Mark, Course
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy, reverse
from core.decorators import teacher_required


@teacher_required
def projects_list(request):
    # good to know - capital letters have priority over lowercase one in alphabetical sorting
    project_list = Project.objects.order_by('name')
    query = request.GET.get('q')
    if query:
        project_list = Project.objects.filter(
            Q(name__icontains=query)
        ).distinct()

    paginator = Paginator(project_list, 15)  # 15 project per page
    page = request.GET.get('page')

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    context = {
        'projects': projects
    }
    return render(request, "projects/project_list.html", context)


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('project_list')

    def form_valid(self, form, **kwargs):
        form.instance.teacher = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(UpdateView):
    model = Project
    fields = ('name', 'summary')
    success_url = reverse_lazy('project')

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('project', kwargs={'pk': pk})


def projects(request, pk):
    projects_data = Project.objects.get(id=pk)
    courses = Course.objects.filter(project=pk)
    context = {
            'project': projects_data,
            'courses': courses,
        }
    return render(request, 'projects/project.html', context)


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm

    def form_valid(self, form, **kwargs):
        form.instance.teacher = self.request.user
        form.instance.project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.project.pk
        return reverse('project', kwargs={'pk': pk})
