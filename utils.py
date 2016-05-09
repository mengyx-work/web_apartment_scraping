from os.path import join
import string, random, yaml

MIN_LENGTH = 10
YML_FILE_PATH = './config/data.yml'

def GenPassword(length):
    lett_candidates = string.uppercase + string.lowercase + string.punctuation
    lett_index = range(0, len(lett_candidates))
    random.shuffle(lett_index)
    length =  length if length > MIN_LENGTH else MIN_LENGTH
    return ''.join([lett_candidates[i] for i in lett_index[:length]])

def GenYamlData(pass_length = 16):
    password = GenPassword(pass_length)
    rpc_xml_yml = {'server_password': password, 'db_host':'localhost',
            'db_port':27017, 'database_name':'craiglist_content_db', 'collection_name':'craiglist_apartment_info'}

    yml_data = {'rpc-xml_server':rpc_xml_yml}
    with open(YML_FILE_PATH, 'w') as f:
        f.write(yaml.dump(yml_data, default_flow_style=False))

def GetYamlData(dict_key):
    with open(YML_FILE_PATH, 'r') as stream:
        yml_content = yaml.load(stream)   
    if dict_key in yml_content.keys():
        return yml_content[dict_key]
    else:
        raise ValueError('the dict_key is missing in yml file')


