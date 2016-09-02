# feeder

```bash
mkvirtualenv --no-site-packages --python=/usr/local/Cellar/python3/3.5.2_1/bin/python3 feeder

env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" \
  pip install --upgrade -r requirements.txt
```
