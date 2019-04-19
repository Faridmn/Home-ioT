# stl
import os

# pip
import yaml

def load_yml_to_dict(fname: str) -> dict:
    assert os.path.isfile(fname)
    with open(fname, 'r') as f:
        print(f'Loading {fname}')
        return yaml.load(f, Loader=yaml.FullLoader)
