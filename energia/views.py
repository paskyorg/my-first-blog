from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
import datetime
from . import utils

# Create your views here.

def listado(request):
    if request.POST:
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)
    return render(request, 'listado.html', {})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Aquí tratamos el archivo con una función
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                print('No parece un archivo CSV')
            data = utils.parseCSV(csv_file)
            return render(request, 'upload.html', {'form': form, 'data': data})
    else:
        print("not POST method")
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})