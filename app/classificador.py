
"""  """

import xgboost as xgb
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
import pandas as pd

from settings import *


def cria_modelo(df):
    """ Instancia e treina um modelo XGBClassifier

        Args
            df: Dataframe com valores a serem usados para treinar
            o classificador

        returns
            Uma tuple com modelo treinado e sua pontuação em caso
            de sucesso, caso contrário retorna None
    """

    try:
        colunas = df.columns

        # Separa X e y
        X = df.drop(colunas[-1], axis=1)
        y = df[colunas[-1]]

        # Instancia modelo classificador
        clf = xgb.XGBClassifier(nthread=-1)

        # Treina modelo
        clf.fit(X, y)

        # Salva modelo
        joblib.dump(clf, 'model/0001.model')

        return clf, cross_val_score(clf, X, y, cv=5).mean()

    except xgb.core.XGBoostError as e:
        print(e)
        return None, None


def avalia_feature(rotulos, **kwargs):
    """ Realiza uma avaliaçao
        Recebe como parâmetro um dicionarios de features
    """

    # Carrega classificador
    model = carrega_modelo()

    X = [[round(float(kwargs[e]), 3) for e in rotulos]]
    a = model.predict(pd.DataFrame(X, columns=rotulos))
    return a


def carrega_modelo(path_model=PATH_MODEL):
    """ Carrega o modelo salvo em arquivo

        Args:
            Caminho do modelo salvo

        Returns:
            O modelo carregado
    """
    return joblib.load(PATH_MODEL)
