import time

from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.views import View

from .forms import FileForm
from .models import File


class BasicUploadView(View):
    def get(self, request, pk):
        pk = pk
        files_list = File.objects.all()
        return render(self.request, 'upload/basic_upload/index.html', {'files': files_list, 'pk': pk,})

    def post(self, request, pk):
        form = FileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            form.instance.course = pk
            form.instance.sender = request.user
            file = form.save()
            data = {'is_valid': True, 'name': file.file.name, 'url': file.file.url, 'sender': file.sender,}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def clear_database(request):
    for file in File.objects.all():
        file.file.delete()
        file.delete()
    return HttpResponseRedirect(request.POST.get('next'))

