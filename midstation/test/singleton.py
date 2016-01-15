# -*- coding: utf-8 -*-
#
# class Singleton(object):
#     def __new__(cls,*args,**kwargs):
#         if not hasattr(cls,'_inst'):
#             cls._inst=super(Singleton,cls).__new__(cls,*args,**kwargs)
#         return cls._inst
import warnings
try:
    import redis
except ImportError:
    redis = None

__all__ = ('Redis', 'FlaskRedis')
__version__ = '0.1.0'


class FlaskRedies(object):
    def __init__(self, app=None, strict=False, config_prefix='REDIS'):
        self._provider_class = None
        self._redis_client = None
        self.config_prefix = config_prefix

    def init_app(self, app, strict=False):
        if self._provider_class is None:
            self._provider_class = (
                redis.StrictRedis if strict else redis.Redis
            )

        redis_url = app.config.get(
            '{0}_URL'.format(self.config_prefix), 'redis://localhost:6379/0'
        )
        db = app.config.get('{0}_DATABASE'.format(self.config_prefix))

        if db is not None:
            warnings.warn(
                'Setting the redis database in its own config variable is'
                'deprecated. Please include it in the URL variable instead.',
                DeprecationWarning,
            )

        self._redis_client = self._provider_class.from_url(redis_url, db=db)

        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['redis'] = self

    def __getattr__(self, item):
        return getattr(self._redis_client, item)


