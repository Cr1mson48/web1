import os
 
from_email = 'wqisup@gmail.com'
password = 'Yq5-4DY-eJw-CMq'
REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
print(REDIS_URL)