import os
from typing import List
from config import get_config
import models
config = get_config()
def list_files(path: str) -> List[str]:
    try:
        files = sorted(os.listdir(path))
    except:
        raise Exception(f'Unable to read path {path}')

    return files

def migrate_files(movie: models.Movie, adding: bool = True):
    base_current = config['imports'] if adding else config['movies']
    base_new = config['movies'] if adding else config['imports']

    path_current = f'{base_current}/{movie.filename}'
    path_new = f'{base_new}/{movie.filename}'
    os.rename(path_current, path_new)