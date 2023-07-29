import os
from typing import Dict
import yaml
import sys

DEFAULT_CONFIG_PATH = "./config.yaml"
def run_once(f):
    def helper(*args, **kwargs):
        if not helper.has_run:
            helper.has_run = True
            helper.data = f(*args, **kwargs)

        return helper.data
    helper.has_run = False
    return helper

@run_once
def get_config() -> Dict[str, str]:
    path = os.getenv('MM_CONFIG_PATH', DEFAULT_CONFIG_PATH)

    try:
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
            return data
    except:
        print(
            f'failed to read the config file{path}',
            file=sys.stderr,
        )