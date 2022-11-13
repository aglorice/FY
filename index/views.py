from django.shortcuts import render

# Create your views here.
from api.models import Fy


def index(request):
    citys = ''
    city = Fy.objects.values('city')
    for i in city:
        citys = i['city']
    return render(request, "index.html", locals())
