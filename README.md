# feeder

## Setup

Prepare Python3 with virtualenv wrapper.

```bash
mkvirtualenv --no-site-packages --python=/usr/local/Cellar/python3/3.5.2_1/bin/python3 feeder

env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" \
  pip install --upgrade -r requirements.txt
```

Initialize PostgreSQL database

```bash
initdb -E utf8 db/pg-data -U postgres
psql -U postgres -c "CREATE DATABASE feeder_dev;"
```
