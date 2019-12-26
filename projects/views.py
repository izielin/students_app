from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import ProjectForm, CourseForm, FileForm, TakePartForm
from .models import Project, File, Course
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy, reverse
from core.decorators import teacher_required
from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.views import View
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalReadView, BSModalDeleteView
from profiles.models import Profile
from django.forms.models import model_to_dict

# @teacher_required
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


def projects_list_for_students(request):
    project_list = Project.objects.order_by('name')
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
    return render(request, "projects/projects_list_for_students.html", context)


class ProjectCreateView(BSModalCreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('project_list')

    def form_valid(self, form, **kwargs):
        form.instance.teacher = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(BSModalUpdateView):
    model = Project
    template_name = 'projects/project_update_form.html'
    success_url = reverse_lazy('project')
    form_class = ProjectForm
    success_message = 'Success: Project was updated.'

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('project', kwargs={'pk': pk})

    def form_valid(self, form, **kwargs):
        form.instance.teacher = self.request.user
        return super().form_valid(form)


class ProjectDeleteView(BSModalDeleteView):
    model = Project
    template_name = 'projects/project_delete.html'
    success_message = 'Success: Project was deleted.'
    success_url = reverse_lazy('project_list')


class ProjectReadView(BSModalReadView):
    model = Project
    template_name = 'projects/project_shortcut.html'

    def post(self, request, pk):
        if request.method=='POST':
            project = Project.objects.filter(pk=pk)
            obj = Profile.objects.get(user=self.request.user)
            obj.projects.set(project)
            obj.save()
            data = {'is_valid': True, 'project': str(project),}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


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
    template_name = 'projects/course_form.html'
    success_message = 'Success: Course was created.'

    def form_valid(self, form, **kwargs):
        form.instance.teacher = self.request.user
        form.instance.project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.project.pk
        return reverse('project', kwargs={'pk': pk})


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('course')

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('course', kwargs={'pk': pk})

    def form_valid(self, form, **kwargs):
        form.instance.teacher = self.request.user
        return super().form_valid(form)


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('project')

    def get_success_url(self):
        pk = self.object.project.id
        return reverse('project', kwargs={'pk': pk})


class CourseView(View):
    def get(self, request, pk):
        course_data = Course.objects.get(id=pk)
        context = {
            'files': File.objects.filter(course=pk),
            'course': course_data,
            'pk': pk,
        }
        return render(self.request, 'projects/course.html', context)

    def post(self, request, pk):
        form = FileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            form.instance.course = pk
            form.instance.sender = request.user
            file = form.save()
            data = {'is_valid': True, 'name': file.file.name, 'url': file.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def delete_file(request, pk):
    for file in File.objects.filter(id=pk):
        file.file.delete()
        file.delete()
    return HttpResponseRedirect(request.POST.get('next'))
