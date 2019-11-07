from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView
from .forms import ProjectForm, MarkForm, CourseForm
from .models import Project, Mark, Course
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy


def projects_list(request):
    project_list = Project.objects.all()
    query = request.GET.get('q')
    if query:
        project_list = Project.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).distinct()

    paginator = Paginator(project_list, 15)  # 15 profiles per page
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
    success_url = reverse_lazy('project')

    # def form_valid(self, form, **kwargs):
    #     form.instance.project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
    #     print(form.instance.project)
    #     return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.project.pk
        return reverse_lazy('project', kwargs={'pk': pk})
