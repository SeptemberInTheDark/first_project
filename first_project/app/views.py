from django.shortcuts import get_object_or_404, render

from .models import Phone

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
