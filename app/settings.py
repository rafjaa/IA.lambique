

UPLOAD_FOLDER = 'dataset'
ALLOWED_EXTENSIONS = {'csv'}
NUM_ROUND = 2

# paramgrid = {'n_estimators': [10, 100, 1000],
#             'max_depth': [3, 5, 10],
#             'learning_rate': [0.1, 0.01, 0.001]}

paramgrid = {'n_estimators': [100]}

# Arquivo de informações da sessão
INFO = '.info'

PATH_MODEL = 'model/0001.model'
