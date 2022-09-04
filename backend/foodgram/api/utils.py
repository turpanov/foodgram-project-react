import csv

from django.db.models import Sum
from django.http.response import HttpResponse


def download_csv_shopping_cart(recipe_ingredient):
    ingredients = recipe_ingredient.values(
        'ingredient_id__name', 'ingredient_id__measurement_unit'
    ).annotate(ingredient_amount=Sum('amount')).values_list(
        'ingredient_id__name', 'amount',
        'ingredient_id__measurement_unit',
    )
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = ('attachment;'
                                       'filename="Shoppingcart.csv"')
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    for item in list(ingredients):
        writer.writerow(item)
    return response
