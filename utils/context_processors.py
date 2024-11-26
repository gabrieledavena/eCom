from store.models import Category, Marca


def range_size(request):
    return {'range_size': range(37, 46),'category_range': Category.objects.all(),'marca_CHOICES': Marca.objects.all()}