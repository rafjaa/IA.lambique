import os
from math import ceil

from flask import Flask, request, flash, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from random import randrange
import json
from sklearn import preprocessing

from classificador import cria_modelo, cria_modelo_otimizado, avalia_feature
from classificador import carrega_modelo
from settings import *


# Servidor HTTP
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'some_secret'
app.debug = True

# Caminho para gráfico features importance
GRAFICO_F_IMPORTANCE = 'static/img/features_importance.png'

# Caminho para gráfico variação dos parâmetros
GRAFICO_V_PARAMETROS = 'static/img/variacao.png'

# Caminho para gráfico matriz correlação
GRAFICO_M_CORRELACAO = 'static/img/m_corr.png'


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


@app.route('/')
@app.route('/dados', methods=["GET", "POST"])
def index():
    """ Caso seja utilizado o método GET há renderização da página
        de inserção do conjunto de dados, caso seja utilizado POST
        é carregado o arquivo csv de entrada, em caso de sucesso,
        o usuário é redirecionado para página de análise
    """
    if request.method == 'POST':

        file = request.files['file']

        # Verifica se foi selecionado algum arquivo
        if file.filename == '':
            flash('Nenhum arquivo foi selecionado!')
            return redirect(request.url)

        # Verifica a extensão do arquivo
        if not allowed_file(file.filename):
            flash('Arquivo invalido!')
            return redirect(request.url)

        flash('O arquivo foi enviado com sucesso!')

        # Salva o arquivo selecionado
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if os.path.exists(INFO):
            os.remove(INFO)

        return redirect(url_for('analise', filename=filename))

    else:
        return render_template('dados.html')


@app.route('/analise/otimiza', methods=['GET'])
def otimiza():
    """ Cria um modelo otimizado

        Returns:
            Renderiza a página de análise
    """
    try:
        # Obtém o nome do arquivo de entrada
        file = obtem_informacao(INFO, 'filename')['filename']

        # Abre aquivo de entrada e o armazena no DataFrame
        df = pd.read_csv('{0}/{1}'.format(UPLOAD_FOLDER, file), sep=',')

        modelo, pontuacao = cria_modelo_otimizado(df)

        # Gráfico de importancia dos parâmetros
        plot_features_importance(modelo)

        # Altera no arquivo de informação o status de otimizado
        # e a pontuação do classificador
        salva_informacao(pontuacao=pontuacao, otimizado=True)

    except (TypeError, FileNotFoundError):
        print('Falha ao ler csv')

    return render_template(
        'analise.html', df='', n=randrange(1000),
        otimizado=True, pontos=pontuacao
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


@app.route('/analise', methods=['GET', 'POST'])
def analise():
    """ Cria um modelo
        Returns:
            Renderiza a página de análise
    """
    modelo = None
    file = None
    otimizado = None
    pontuacao = None
    dict_info = None

    try:

        dict_info = obtem_informacao(INFO, 'otimizado', 'pontuacao')
        otimizado = dict_info['otimizado']
        pontuacao = dict_info['pontuacao']

    except (TypeError):
        otimizado = False

    if 'filename' not in request.args:
        try:
            modelo = carrega_modelo()
        except FileNotFoundError:
            # Selecione arquivo em caso de falha
            flash('Nenhum modelo foi criado, selecione os dados para análise!')
            return redirect('/dados')

    else:
        try:
            file = request.args['filename']

            # Abre aquivo de entrada e o armazena no DataFrame
            df = pd.read_csv('{0}/{1}'.format(UPLOAD_FOLDER, file), sep=',')

            # Pré-processa arquivo de entrada
            df, dict_classes = pre_processa_entrada(df)

            # Persiste o DataFrame pré-processado
            df.to_csv('{0}/{1}'.format(UPLOAD_FOLDER, file), index=False)

            modelo, pontuacao = cria_modelo(df)

            if modelo is None:
                flash('Algum erro ocorreu na criação do modelo!')
                return redirect('/dados')

            # Gráfico de correlação
            plot_matriz_correlacao(df, GRAFICO_M_CORRELACAO)

            # Gráfico variação de parâmetros
            plot_variacao_parametros(df, GRAFICO_V_PARAMETROS)

            # Gráfico de importância dos parâmetros
            plot_features_importance(modelo, GRAFICO_F_IMPORTANCE)

            features = []

            # Salva a informação das colunas dos dados de entrada,
            # para serem usadas na simulação
            for column in df.columns[:-1]:
                features.append({
                    'nome': column,
                    'max': float(df[column].max()),
                    'min': float(df[column].min()),
                    'media': round(float(df[column].mean()), 3)
                })

            salva_informacao(**{
                'filename': file, 'modelo': 'model/0001.model',
                'otimizado': False, 'pontuacao': pontuacao,
                'features': features, 'dict_classes': dict_classes
            })

        except FileNotFoundError as e:
            flash('O arquivo não pode ser aberto!')
            print(e)

        except pd.errors.EmptyDataError:
            flash('O arquivo csv está vazio!')
            return redirect('/dados')

        except ValueError as e:
            flash('Dados insuficientes!', e)
            return redirect('/dados')

    return render_template(
        'analise.html', df='', n=randrange(1000),
        file=file, otimizado=otimizado, pontos=pontuacao
    )


@app.route('/simulacao', methods=['GET', 'POST'])
def simulacao():
    """ Renderiza uma página para realizar a simulação onde é
        possível inserir diferentes valores de entrada e receber uma
        predição do valor esperado com base no modelo salvo

        Returns:
            Renderiza a página de simulação
    """

    nota = None

    # Carrega o arquivo de informações dos dados de entrada
    features = obtem_informacao(INFO, 'features')

    # Verifica falha na leitura das features
    if features is None:
        flash('Erro no arquivo!')
        return redirect('/dados')

    features = features['features']

    # Caso seja realizado uma requisição POST, realiza-se a avaliação
    if request.method == 'POST':
        form_data = request.form.to_dict()
        nota = avalia_feature([f['nome'] for f in features], **form_data)

    return render_template('base.html', features=features, nota=nota)


def plot_variacao_parametros(df, path):
    """ Salva a variação dos parâmetros do DataFrame para um arquivo
        em formato .png

        Args:
            df: DataFrame utilizado no cálculo da variação dos parâmetros
            path: caminho onde será salva o arquivo

    """
    # Agrupa pela última coluna e obtém a média destes valores
    df_mean = df.groupby(df.columns[-1]).mean()

    # Define configurações do gráfico
    rows, cols = df_mean.shape
    nrows = ceil(cols / 3)
    ncols = cols if cols < 3 else 3

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, nrows * 4))
    axes_list = axes.flatten()
    fig.suptitle("Variação dos parâmetros")

    # Aumenta espaço entre gráficos
    fig.subplots_adjust(hspace=0.4, wspace=0.3)

    # Plota gráfico com média dos elementos, agrupado pela nota
    for i, column in enumerate(df_mean.columns):
        ax = axes_list[i]
        ax.set_title(column)
        df_mean[column].plot(ax=ax, kind="line")

    # Salvando a figura do gráfico criado
    plt.savefig(path)


def plot_matriz_correlacao(df, path):
    """ Salva a matriz de correlação do DataFrame para um arquivo
        em formato .png

        Args:
            df: DataFrame utilizado no cálculo da matriz de correlação
            path: caminho onde será salva o arquivo

    """
    # Calcula a correlação
    corr_mat = df.corr()

    f, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(corr_mat, vmax=.2, square=True, annot=True)

    # Salvando a figura do gráfico criado
    plt.savefig(path)


def plot_features_importance(modelo, path):
    """ Salva um arquivo em formato .png com a importância dos parâmetros

        Args:
            modelo: modelo utilizado na geração do gráfico
            path: caminho onde será salva o arquivo
    """
    xgb.plot_importance(modelo)
    plt.savefig(path)


def salva_informacao(path=INFO, **kwargs):
    """ Salva as informações em arquivo

        Args:
            path: Caminho onde o arquivo será salvo
            **kwargs: Lista de parâmetros a ser salva
    """
    try:
        arq = kwargs

        if os.path.exists(path):
            arq = json.load(open(path))
            arq.update(kwargs)

        with open(path, 'w') as f:
            f.write(json.dumps(arq))

    except json.decoder.JSONDecodeError:
        print('Erro ao gravar informação do dataset!')


def obtem_informacao(path=INFO, *args):
    """ Retorna as informações salvas em arquivo

        Args:
            path: Caminho onde o arquivo será salvo
            **kwargs: Lista de parâmetros a ser salva
    """
    try:
        dict_info = None
        print(path, args)

        if os.path.exists(path):
            arq = json.load(open(path))

            if len(args):
                dict_info = {k: v for (k, v) in arq.items() if k in args}
            else:
                dict_info = arq

        return dict_info

    except json.decoder.JSONDecodeError:
        print('Erro ao recuperar informação do dataset!')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
