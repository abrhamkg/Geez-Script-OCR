import configparser

config = configparser.ConfigParser()


def get_params(config, config_name, items):
    return [config[config_name][i] for i in items]


if __name__ == '__main__':
    config['DEFAULT'] = {'MODEL_DIR': 'models',
                         'DATA_DIR': 'data',
                         'MORPHOLOGY_KERNEL':'RECT',
                         'MORPH_KERNEL_SIZE': '(3, 11)',
                         'BILATERAL_FILTER': '0',
                         'MODE': 'DEBUG',
                         }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
