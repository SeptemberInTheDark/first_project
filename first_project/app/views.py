from django.shortcuts import get_object_or_404, render

from .models import Phone, Sensor, Measurement 
from rest_framework import generics
from .serializers import (
    SensorSerializer,
    SensorDetailSerializer,
    MeasurementSerializer,
)
from app.models import *

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}


def index(request):
    return render(request, 'index.html')

def get_omlet(request):
    context = {'recipe': DATA.get('omlet')}
    return render(request, 'omlet.html', context)

def get_pasta(request):
    context = {'recipe': DATA.get('pasta')}
    return render(request, 'pasta.html', context)


def catalog(request):
    sort = request.GET.get('sort')
    phones = Phone.objects.all()

    if sort == 'name':
        phones = phones.order_by('name')
    elif sort == 'min_price':
        phones = phones.order_by('price')
    elif sort == 'max_price':
        phones = phones.order_by('-price')

    return render(request, 'catalog.html', {'phones': phones})


def phone(request, slug):
    phone_obj = get_object_or_404(Phone, slug=slug)
    return render(request, 'product.html', {'phone': phone_obj})



class SensorListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/sensors/  -> список датчиков
    POST /api/sensors/  -> создать датчик
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    GET   /api/sensors/<id>/ -> датчик с измерениями
    PATCH /api/sensors/<id>/ -> частичное обновление
    PUT   /api/sensors/<id>/ -> полное обновление
    """
    queryset = Sensor.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SensorDetailSerializer
        return SensorSerializer


class MeasurementCreateView(generics.CreateAPIView):
    """
    POST /api/measurements/ -> добавить измерение
    body: { "sensor": <id>, "temperature": <value> }
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


########################################################
def students_list(request):
    template = 'school/students_list.html'
    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    ordering = 'group'
    from .models import Student
    students = Student.objects.all().order_by(ordering, 'name')
    context = {
        'object_list': students,
    }
    return render(request, template, context)


########################################################
def articles_list(request):
    template = 'articles/news.html'
    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    ordering = '-published_at'
    articles = Article.objects.all().order_by(ordering).prefetch_related('scopes__tag')
    context = {
        'object_list': articles,
    }
    return render(request, template, context)