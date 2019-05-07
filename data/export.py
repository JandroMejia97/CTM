import pandas as pd
import os
#from apps.calculadora.models import Pais, Ciudad, Continente, IdiomaOficial, MonedaOficial

def import_data(file):
    url = os.getcwd()+'/'+file
    data = pd.read_csv(url, encoding="ISO-8859-1", engine='python')
    print(data)
    columnas = [
        'ISO3166_1_numeric',
        'ISO4217_currency_numeric_code',
        'Capital',
        'Languages'
    ]
    print(data)
    data = data.drop(columns=columnas)
    for row in data.itertuples(index=False):
        print(row)
        c = Continente.objects.get(
            codigo=row.Continent
        )

        p = Pais.objects.update_or_create(
            nombre=row.official_name_es,
            iso_3166_1_2=row.ISO3166-1-Alpha-2,
            iso_3166_1_3=row.ISO3166-1-Alpha-3,
            continente=c
        )

def export_data(file, col):
    url = os.getcwd()+'/'+file
    data = pd.read_csv(url)
    print(data.head())
    data=data.drop(columns=col)
    print(data.head())
    data.to_csv('country_new.csv', index=False)

name = 'country_new.csv'
import_data(name)