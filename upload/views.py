import time

from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.views import View

from .forms import FileForm
from .models import File


class BasicUploadView(View):
    def get(self, request):
        files_list = File.objects.all()
        return render(self.request, 'upload/basic_upload/index.html', {'files': files_list})

    def post(self, request):
        form = FileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            file = form.save()
            data = {'is_valid': True, 'name': file.file.name, 'url': file.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def clear_database(request):
    for file in File.objects.all():
        file.file.delete()
        file.delete()
    return HttpResponseRedirect(request.POST.get('next'))

