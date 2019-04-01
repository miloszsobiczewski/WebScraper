from django.shortcuts import render
from .models import Task
from .forms import TaskForm
import pdb
from . import utils as ut
import random
from web_scraper.settings import STATIC_URL


# Create your views here.
def webscraper(request):
    if request.method == 'POST':
        taskform = TaskForm(request.POST)
        if taskform.is_valid():
            instance = taskform.save(commit=False)
            instance.status = 'initialized'
            instance.save()
            url = instance.url
            # scraping txt data
            if taskform.cleaned_data['txt_ind']:
                instance.status = 'scraping text'
                instance.save()
                hash = random.getrandbits(32)
                file_name = \
                    STATIC_URL + 'webscraper/text_' + str(hash) + '.txt'
                res = ut.save_txt(file_name[1:], url)
                if res:
                    instance.status = 'saving txt complete'
                    instance.save()
                    instance.txt_slug = file_name
                else:
                    result = 'Task failed!'
                    instance.status = 'saving txt failed'
                    instance.save()
                    return render(request, 'webscraper/home.html',
                                  {'taskform': taskform, 'result': result})

            # scraping images
            if taskform.cleaned_data['img_ind']:
                instance.status = 'scraping images'
                instance.save()
                val = ut.save_img(url)
                # is_success, images = ut.save_img(url)

                if val[0]:
                    if len(val[1]) == 0:
                        instance.status = 'no image found'
                        instance.save()
                        instance.img_ind = False
                    else:
                        instance.status = 'saving img complete'
                        instance.save()
                        # convert list to string
                        images = ['/%s' % v for v in val[1]]
                        instance.img_slug = str(images)[1:-1].replace("'", "")
                else:
                    result = 'Task failed!'
                    instance.status = 'saving img failed'
                    instance.save()
                    return render(request, 'webscraper/home.html',
                                  {'taskform': taskform, 'result': result})

            instance.status = 'complete'
            instance.save()
            result = 'Task #%s succeed!' % instance.pk
        else:
            result = 'Form validation failed'
    else:
        result = 'Ready to schedule task'
        taskform = TaskForm()
    return render(request, 'webscraper/home.html', {'taskform': taskform,
                                                    'result': result})


def status(request):
    data = Task.objects.all().order_by('-id')
    return render(request, 'webscraper/tasks.html', {'data': data})


def site(request):
    return render(request, 'webscraper/site.html')