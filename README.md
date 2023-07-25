# Declare and load configuration the robust way in Python

**THIS IS NOT A LIBRARY, BUT A DEMO APP YOU CAN COPY AND MODIFY TO FIT YOUR NEEDS.**

Highlights:

* Configuration is declared as Pydantic models,
* So how to write/update the configuration file is clear,
* And mistakes are easily found by Pydantic's validation.
* The default configuration file is `~/.myapp.yaml`,
* Which can be overridden by `MYAPP_CONFIGURATION_FILE` environment variable.
* The `myapp.conf.settings` object holds your configuration,
* Which is an object with strong schema (not like a dict).
* The `settings` can be refreshed by `refresh()` method to reflect configuration changes.

## Step 1 - Declare your configuration as Pydantic models

As in `myapp/conf.py`, change the `Settings` model definition to match your needs. The version you see came from my real projects.

## Step 2 - Write your configuration file

The configuration is loaded from `~/.myapp.yaml` by default, and can be overridden via the `MYAPP_CONFIGURATION_FILE` environment variable.

Follow the example declaration, the configuration content can be:

```yaml
dev_mode: false

db:
  host: wonder-dev
  port: 5432
  user: myapp
  password: myapp
  database: myapp

caches:
  default:
    backend: fs
    cache_dir: /tmp/myapp-cache
```

## Step 3 (Optional) - Inspect the loaded `settings` object

```python
from myapp.conf import settings
settings
```

Output:

```python
Settings(dev_mode=False, db=DB(host='wonder-dev', port=5432, database='myapp', user='myapp', password='myapp', pool_size=4, max_overflow=20, echo_sql=False), caches={'default': FsCache(backend='fs', cache_dir='/tmp/myapp-cache', threshold=None, default_timeout=None)}, logging=None)
```

## Step 4 - Use the `settings` object to build your application modules

Take the `db` module for example, there maybe the `db.py` file in your project:

```python
import sqlalchemy as sa

from myapp.conf import settings

dbc = settings.db

db_url = f"postgresql+psycopg2://{dbc.user}:{dbc.password}@{dbc.host}:{dbc.port}/{dbc.database}"

engine = sa.create_engine(
    db_url, pool_size=dbc.pool_size, max_overflow=dbc.max_overflow, echo=dbc.echo_sql,
)
...
```
