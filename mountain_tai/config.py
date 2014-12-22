# from settings import DATABASES
# from settings import SECRET_KEY
import redis
SECRET_KEY = '6vv0xbhmm(02ru1t*ztb-499^gnn_nrwc-is1^sv#j%ki*c9cw'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'telegraph_pole',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': '',
    }
}
rediscon = redis.Redis(host="127.0.0.1", port=6379, db=0)
