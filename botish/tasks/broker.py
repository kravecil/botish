from taskiq_redis import RedisStreamBroker
from botish.settings import settings

broker = RedisStreamBroker(url=settings.redis_dsn.encoded_string())
