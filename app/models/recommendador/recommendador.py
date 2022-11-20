from ast import literal_eval
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

from config.default import RUTA_SAVE


def load_csv_pokemon():
    lista = ['index', 'pokedex_id', 'name', 'hp', 'attack', 'defense', 'special', 'speed', 'tipos']
    df = pd.read_csv('pokemon_csv6.csv', sep=';', names=lista, engine='python')

    # La columna tipos se lee como un string "[]", para que se una lista hacemos el apply
    df.tipos = df.tipos.apply(literal_eval)
    return df


class Recomendador:
    def __init__(self, dataframe):
        self.dataframe = dataframe.sort_values(by=['pokedex_id']).reset_index(drop=True)
        self.df_cosine = self.load()

    def create_dummies_tipos(self):
        '''
        Create dummies de los tipos de los pokemons
        :param dataframe:
        :return:
        '''
        df_tipos = self.dataframe[['pokedex_id', 'tipos']]
        dummies_df = pd.get_dummies(
            df_tipos.join(pd.Series(df_tipos['tipos'].apply(pd.Series).stack().reset_index(1, drop=True),
                                    name='tipos1')).drop('tipos', axis=1).rename(columns={'tipos1': 'tipos'}),
            columns=['tipos']).groupby('pokedex_id', as_index=False).sum()
        return dummies_df

    def scale(self):
        scaler = StandardScaler()
        scaled_df = scaler.fit_transform(
            self.dataframe.drop(columns=['index', 'pokedex_id', 'name', 'tipos']))
        scaled_df = pd.DataFrame(scaled_df, columns=['hp', 'attack', 'defense', 'special', 'speed'])
        return scaled_df

    def join_dataframes(self):
        new_poke_df = pd.concat([self.create_dummies_tipos(), self.scale()], axis=1)
        return new_poke_df.drop(columns=['pokedex_id'])

    def cosine_similarity(self):
        cos_sim = cosine_similarity(self.join_dataframes().values, self.join_dataframes().values)
        self.save(cos_sim)
        return cos_sim

    @staticmethod
    def load():
        my_file = Path(RUTA_SAVE + 'cosine_similarity.csv')
        if my_file.exists():
            return pd.read_csv(RUTA_SAVE + 'cosine_similarity.csv')

    @staticmethod
    def save(matrix):
        matrix.to_csv(RUTA_SAVE + 'cosine_similarity.csv')

    def get_index_pokemon(self, pokedex_id):
        poke_index = pd.Series(self.dataframe.index, index=self.dataframe['pokedex_id'])
        return poke_index[pokedex_id]

    def recommend(self, pokedex_id, recommendations=5):
        index = self.get_index_pokemon(pokedex_id)
        if not self.df_cosine:
            self.df_cosine = self.cosine_similarity()
        similarity_score = list(enumerate(self.df_cosine[index]))
        sorted_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
        similar_pokemon = sorted_score[1:recommendations + 1]
        poke_indices = [i[0] for i in similar_pokemon]
        return self.dataframe.iloc[poke_indices].to_dict(orient="records")

