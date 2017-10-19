import os

from flask import Flask, request, flash, render_template
from werkzeug.utils import secure_filename
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import xgboost as xgb
import json
from sklearn import preprocessing
from tinydb import Query, TinyDB

from classificador import cria_modelo, avalia_feature
from settings import *

matplotlib.style.use('ggplot')

# Servidor HTTP
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'some_secret'
app.debug = True

# Caminho para gráfico features importance
GRAFICO_F_IMPORTANCE = 'static/img/features_importance.png'

# Define local para savar informações
User = Query()
db = TinyDB('db.json')
table = db.table('info')

# Cria diretório de dataset
if not os.path.exists('dataset'):
    os.mkdir('dataset')


def allowed_file(filename):
    """ Verifica extensão do arquivo de entrada

        Args:
            filename: nome do arquivo de entrada

        Returns:
            True se a extensão for permitida e
            False caso contrário
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    ''' Exibe página principal '''

    return render_template('index.html')


@app.route('/info', methods=['GET'])
def info():
    ''' '''

    return json.dumps(table.all()[0])


@app.route('/dados', methods=["POST"])
def dados():
    """ Caso seja utilizado o método GET há renderização da página
        de inserção do conjunto de dados, caso seja utilizado POST
        é carregado o arquivo csv de entrada, em caso de sucesso,
        o usuário é redirecionado para página de análise
    """
    if request.method == 'POST':
        file = request.files['file']

        # Verifica se foi selecionado algum arquivo
        if file.filename == '':
            return json.dumps({'erro': 'Nenhum arquivo!'})

        # Verifica a extensão do arquivo
        if not allowed_file(file.filename):
            return json.dumps({'erro': 'Arquivo invalido!'})

        # Salva o arquivo selecionado
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        status, resul, fscore = processa(filename)

        return json.dumps(
            {'status': status, 'pontuacao': resul, 'fscore': fscore}
        )


def categoriza_rotulos(y_labels):
    """ Transforma rótulos não numéricas em numéricas

        Args:
            y_labes: numpy type contendo valores a serem transformados

        returns
            Uma tuple de dois elementos. No index 0 um array numpy com y_labels
            transformados e no index 1 um dict com resultados do le associado
            às classes.

    """
    # Instancia e treina o LabelEncoder
    le = preprocessing.LabelEncoder()
    le.fit(y_labels)

    # Converte retorno para int
    le_transform = map(int, le.transform(le.classes_))

    # Cria dicionario assciando os resultados do le com as classes
    dict_classes = dict(zip(le.classes_, le_transform))

    return le.transform(y_labels), dict_classes


def pre_processa_entrada(df):
    """ Pré-processa o DataFrame de entrada removendo suas linhas nas quais
        possuem valores NaN na última coluna, completando com a média os
        demais valores faltantes e converte valores str para valores númericos.

        Args:
            df: Dataframe a ser pré-processado

        Returns
            Um DataFrame pré-processado e um dict com os rótulos numéricos
            associados aos valores str convertidos
    """
    colunas = df.columns
    dict_classes = {}

    # Apaga as linhas que possuem valor nulo na última coluna
    df.dropna(subset=[colunas[-1]], inplace=True)

    # Separa X e y
    X = df.drop(colunas[-1], axis=1)
    y = df[colunas[-1]]

    # Converte valores str para valores númericos
    for c in X.select_dtypes(include=['object']).columns:
        X[c] = pd.factorize(X[c])[0]

    # Categoriza y, caso seja tipo object
    if y.dtype == 'object':
        y, dict_classes = categoriza_rotulos(y.values)

    # Preenchendo valores nulos em X
    X.fillna(X.mean(), inplace=True)

    # Concatenando X e y
    X[colunas[-1]] = y

    return X, dict_classes


def processa(filename):
    """ Cria um modelo
        Returns:
            Um modelo treinado

        Error:
            0 = Sucesso
            1 = Erro ao treinar o modelo
            2 = Dataset Vazio
            3 = Arquivo não encontrado
    """

    try:

        # Abre aquivo de entrada e o armazena no DataFrame
        df = pd.read_csv('{0}/{1}'.format(UPLOAD_FOLDER, filename), sep=',')

        # Pré-processa arquivo de entrada
        df, dict_classes = pre_processa_entrada(df)

        # Persiste o DataFrame pré-processado
        df.to_csv('{0}/{1}'.format(UPLOAD_FOLDER, filename), index=False)

        modelo, pontuacao = cria_modelo(df)

        if modelo is None:
            return 1, None

        fscore = modelo.booster().get_fscore()

        # Gráfico de importância dos parâmetros
        plot_features_importance(modelo, GRAFICO_F_IMPORTANCE)

        # Salva a informação das colunas dos dados de entrada,
        # para serem usadas na simulação
        features = []
        for column in df.columns[:-1]:
            features.append({
                'nome': column,
                'max': float(df[column].max()),
                'min': float(df[column].min()),
                'media': round(float(df[column].mean()), 3)
            })

        dict_info = {
            'filename': filename, 'modelo': 'model/0001.model',
            'pontuacao': pontuacao, 'features': features,
            'dict_classes': dict_classes, 'fscore': fscore,
        }

        table.update(dict_info) if len(table.all()) == 1 else table.insert(dict_info)

    except FileNotFoundError:
        return 3, None
    except pd.errors.EmptyDataError:
        return 2, None

    return 0, pontuacao, fscore


@app.route('/simulacao', methods=['GET', 'POST'])
def simulacao():
    """ Renderiza uma página para realizar a simulação onde é
        possível inserir diferentes valores de entrada e receber uma
        predição do valor esperado com base no modelo salvo

        Returns:
            Renderiza a página de simulação
    """

    # Carrega o arquivo de informações dos dados de entrada
    # features = obtem_informacao(INFO, 'features')
    features = table.all()[0]

    # Caso seja realizado uma requisição POST, realiza-se a avaliação
    if request.method == 'POST':

        # Obtém dados do formulário
        form_data = request.form.to_dict()

        # Realiza a avaliação
        nota = avalia_feature(
            [f['nome'] for f in features['features']], **form_data
        )

        return json.dumps({'sucesso': True, 'nota': float(nota)})

    # Verifica falha na leitura das features
    if features is None:
        flash('Erro no arquivo!')
        return redirect('/dados')

    features = features['features']

    return json.dumps({'features': features})


def plot_features_importance(modelo, path):
    """ Salva um arquivo em formato .png com a importância dos parâmetros

        Args:
            modelo: modelo utilizado na geração do gráfico
            path: caminho onde será salva o arquivo
    """
    matplotlib.rcParams.update({'font.size': 20})

    fig, ax = plt.subplots(figsize=(25, 15))

    ax = xgb.plot_importance(modelo, ax=ax, grid=False)
    plt.title('Importância dos parâmetros', fontsize=30)
    plt.xlabel('Importância')
    plt.ylabel('Parâmetros')
    plt.savefig(path)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
