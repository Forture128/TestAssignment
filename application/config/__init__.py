import os
from dotenv import load_dotenv

__all__ = ['config']


def get_config(env: str):
    load_dotenv()
    if env == 'local':
        from .local import Config
        return Config()
    elif env == 'preprod':
        # return Config()
        pass


config = get_config(os.getenv("APP_ENV", 'local'))
config.ENV = os.getenv('APP_ENV', 'local')

del get_config
