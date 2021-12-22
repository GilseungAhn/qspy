import pickle
from pkg_resources import resource_filename

# load Name_to_Code.pckl to name_to_code_dict
filepath = resource_filename(__name__, "Name_to_Code.pckl")
with open(filepath, "rb") as f:
    name_to_code_dict = pickle.load(f)

# load Code_to_Name.pckl to code_to_name_dict
filepath = resource_filename(__name__, "Code_to_Name.pckl")
with open(filepath, "rb") as f:
    code_to_name_dict = pickle.load(f)

def code_to_name(code):
    return code_to_name_dict[code]

def name_to_code(name):
    return name_to_code_dict[name]