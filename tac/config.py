import configparser

parser = configparser.ConfigParser()

# load local if exists
try:
    parser.read('config.local.ini')
    filename = 'config.local.ini'
except:
    parser.read('config.ini')
    filename = 'config.ini'

# parse a config file
def parseConfig(section):
    conf = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            conf[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the config file'.format(section))
    return conf