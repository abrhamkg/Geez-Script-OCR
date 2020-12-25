import configparser

config = configparser.ConfigParser()

config['DEFAULT'] = {'MODEL_DIR': 'models',
                     'DATA_DIR': 'data',
                     'MORPHOLOGY_KERNEL':'MORPH_RECT',
                     'MORPH_KERNEL_SIZE': '(1, 20)',
                     'BILATERAL_FILTER': '0',

                     }

with open('config.ini', 'w') as configfile:
    config.write(configfile)
