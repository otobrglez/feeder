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

## Spiders

```bash
scrapy crawl delo -a mode=refresh -a categories=novice -a pages=2
scrapy crawl 24ur -a mode=refresh -a pages=2 -a categories=novice/gospodarstvo -L WARNING
```

## Tools and scripts

```bash
./refresh.sh # Does shallow scrape try to fetch more recent items
./recreate_database.py # Drops existing database and creates new one
```
