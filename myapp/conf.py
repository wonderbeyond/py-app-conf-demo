from typing import Optional, Literal, Union
import os.path
from os import environ

import yaml
from pydantic import BaseModel, ConfigDict

_default_configuration_file_path = os.path.expanduser("~/.myapp.yaml")
_configuration_file_path_env_name = "MYAPP_CONFIGURATION_FILE"


class DB(BaseModel):
    model_config = ConfigDict(extra="forbid")

    host: str = '127.0.0.1'
    port: int = 5432
    database: str = 'myapp'
    user: str = 'myapp'
    password: str = 'myapp'
    pool_size: int = 4
    max_overflow: int = 20
    echo_sql: bool = False


class RedisCache(BaseModel):
    model_config = ConfigDict(extra="forbid")

    backend: Literal['redis'] = 'redis'
    host: str
    port: int
    db: int = 0
    password: Optional[str] = None
    default_timeout: Optional[int] = None
    key_prefix: Optional[str] = None


class FsCache(BaseModel):
    model_config = ConfigDict(extra="forbid")

    backend: Literal['fs'] = 'fs'
    cache_dir: str
    threshold: Optional[int] = None
    default_timeout: Optional[int] = None


class MemoryCache(BaseModel):
    model_config = ConfigDict(extra="forbid")

    backend: Literal['memory'] = 'memory'
    threshold: Optional[int] = None
    default_timeout: Optional[int] = None


class Settings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    """The settings model of the project."""
    dev_mode: bool = False
    db: DB = DB()
    caches: dict[str, Union[RedisCache, FsCache, MemoryCache]] = {}
    logging: Optional[dict] = None

    @classmethod
    def load_settings(cls) -> "Settings":
        with open(environ.get(
            _configuration_file_path_env_name, _default_configuration_file_path)
        ) as f:
            return cls.model_validate(
                yaml.safe_load(f), strict=True,
            )

    def refresh(self):
        """In-place refresh (reload) settings from configuration file."""
        self.__dict__.update(self.load_settings().__dict__)


settings = Settings.load_settings()
