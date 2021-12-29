import pickle
from pkg_resources import resource_filename


## 관리하는 종목 목록 관련 함수
# load Name_to_Code.pckl to name_to_code_dict
filepath = resource_filename(__name__, "Name_to_Code.pckl")
with open(filepath, "rb") as f:
    name_to_code_dict = pickle.load(f)

# load Code_to_Name.pckl to code_to_name_dict
filepath = resource_filename(__name__, "Code_to_Name.pckl")
with open(filepath, "rb") as f:
    code_to_name_dict = pickle.load(f)

def name_list():
    return list(code_to_name_dict.values())

def code_list():
    return list(code_to_name_dict.keys())

def code_to_name(code):
    return code_to_name_dict[code]

def name_to_code(name):
    return name_to_code_dict[name]