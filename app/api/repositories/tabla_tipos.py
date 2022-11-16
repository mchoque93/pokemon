import csv
from typing import List


def initialize_equivalence_dictionary(csv_file:str)->dict:
    file = open(csv_file)
    csvreader = csv.reader(file, delimiter=";")
    header = next(csvreader)
    rows = []
    for row in csvreader:
            rows.append(row)


    diccionario_debilidad_tipos={}
    for row in rows:
        dic = dict(zip(header, row))
        tipo = dic.pop('tipo')
        diccionario_debilidad_tipos[tipo] = {key: float(values.replace(",", ".")) for key,values in dic.items()}
    return diccionario_debilidad_tipos

class EquivalenciaDebilidad:
    def __init__(self, diccionario: dict):
        self.diccionario = diccionario

    def calculate_debilidad(self, pokemon: "Pokemon", diccionario: dict)-> List[str]:
        tipos = pokemon.tipos
        tipos_mas_fuertes = []
        for tipo in tipos:
            stronger_tipos = [key for key,val in diccionario[tipo.name].items() if val == max(diccionario[tipo.name].values())]
            tipos_mas_fuertes += stronger_tipos
        return tipos_mas_fuertes