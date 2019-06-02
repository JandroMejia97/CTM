from apps.calculadora.models import *
from django.db.models import Count

cartas = Carta.objects.filter(restaurante=Restaurante.objects.get(pk=1)).annotate(num_products=Count('producto'))
cartas_padre = TipoCarta.objects.filter(tipo_principal=None)

for carta_padre in cartas_padre:
    print('* ', carta_padre)
    for carta in cartas:
        if carta.tipo.tipo_principal == carta_padre:
            print('  - ', carta.tipo, '\tProductos: ', carta.num_products)
    if carta_padre in cartas:
            print('  - ', carta.tipo, '\tProductos: ', carta.num_products)