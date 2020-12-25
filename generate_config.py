import configparser

config = configparser.ConfigParser()

config['DEFAULT'] = {'MODEL_DIR': 'models',
                     'DATA_DIR': 'data',
                     }

with open('config.ini', 'w') as configfile:
    config.write(configfile)
