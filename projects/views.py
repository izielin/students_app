from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import ProjectForm, CourseForm, FileForm, MarkForm
from .models import Project, File, Course, Mark
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy, reverse
from core.decorators import teacher_required
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.views import View
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalReadView, BSModalDeleteView
from profiles.models import Profile
from django.forms.models import model_to_dict
from django.db.models import FloatField
from django.db.models.functions import Cast


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

    user = Profile.objects.get(user=request.user)
    context = {
        'projects': projects,
        'user': user,
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


def subscribe(request, pk):
    if request.POST.get('action') == 'post':
        project = Project.objects.get(pk=pk)
        obj = Profile.objects.get(user=request.user)
        print(obj.projects.all())
        if project in obj.projects.all():
            obj.projects.remove(project.id)
            print(obj.projects.all())
        else:
            obj.projects.add(project.id)
            print(obj.projects.all())
        obj.save()
        data = {'is_valid': True, 'project': str(project)}
        return JsonResponse(data)


class ProjectReadView(BSModalReadView):
    model = Project
    template_name = 'projects/project_shortcut.html'

    # TODO: call subscribe function (12.12.19)

    # def (self, project_id, **kwargs):
    #     subscribe(self.request, project_id)


def projects(request, pk):
    projects_data = Project.objects.get(id=pk)
    courses = Course.objects.filter(project=pk)
    profile = Profile.objects.get(user=request.user)
    marks = Mark.objects.filter(student=profile.user)
    subscribe(request, pk)

    max_points = sum([i.points for i in courses])
    user_points = sum([i.mark for i in marks])

    context = {
        'project': projects_data,
        'courses': courses,
        'profile': profile,
        'max_points': max_points,
        'user_points': user_points,
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
        teacher = Profile.objects.get(user=course_data.teacher)
        user = self.request.user
        try:
            user_points = Mark.objects.get(student=self.request.user, course=course_data).mark
            max_points = course_data.points
        except Mark.DoesNotExist:
            user_points = ''
            max_points = course_data.points

        files = File.objects.filter(course=pk)
        senders = [i.sender for i in files]
        student = Profile.objects.filter(projects__course__id=course_data.id).order_by('last_name')
        students = [i.user for i in student]
        late = list(set(students)-set(senders))
        late = Profile.objects.filter(user__in=late)
        context = {
            'files': files,
            'course': course_data,
            'teacher': teacher,
            'user': user,
            'user_points': user_points,
            'max_points': max_points,
            'pk': pk,
            'late': late,
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


class MarkCreateView(BSModalCreateView):
    model = Mark
    form_class = MarkForm
    template_name = 'projects/mark.html'
    success_message = 'Success: mark set'

    # TODO: double marks
    def form_valid(self, form, **kwargs):
        form.instance.course = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        course = Course.objects.get(pk=self.kwargs.get('pk'))
        context = super(MarkCreateView, self).get_context_data(**kwargs)
        context['max_mark'] = course.points
        context['course'] = course
        return context

    def get_success_url(self, **kwargs):
        pk = self.object.course.id
        return reverse('course', kwargs={'pk': pk})


def load_students(request):
    course_data = request.GET.get('course')
    file = File.objects.filter(course=course_data)
    senders = [i.sender for i in file]
    student = Profile.objects.filter(projects__course__id=course_data).order_by('last_name')
    students = [i.user for i in student]
    users = list(set(senders).intersection(students))
    return render(request, 'projects/student_dropdown_list_options.html', {'students': users})
