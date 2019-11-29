from ast import literal_eval
from loadconfig import load_config


config = load_config('config/config.yml')
#config = load_config('../config/config.yml')


def getpaths():
    try:
        content = config['api']['paths']
        PATH_DICT = literal_eval(content)

        return PATH_DICT
    except Exception as e:
        print(e)


def getpath(path):
    path_dict = getpaths()
    apiname = path.split('/')[0]
    if apiname in path_dict:
        apipath = path_dict[apiname] + path
        return apipath
    else:
        print('Path not found: ' + path)
        return '404'
