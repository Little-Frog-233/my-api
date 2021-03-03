import os
import sys
import configparser

current_path = os.path.realpath(__file__)
root_path = os.path.dirname(os.path.dirname(current_path))
sys.path.append(root_path)
cfp = configparser.ConfigParser()
cfp.read(os.path.join(root_path, 'conf/web.conf'), encoding='utf-8')
# cfp.read(os.path.join(root_path, 'conf/docker.conf'), encoding='utf-8')


class Config:
    def __init__(self):
        self.base_url = cfp.get('flask', 'base_url')
        self.file_path = cfp.get('flask', 'file_path')
        self.log_path = cfp.get('flask', 'log_path')

        self.sql_host = cfp.get('mysql', 'host')
        self.sql_port = cfp.get('mysql', 'port')
        self.sql_database = cfp.get('mysql', 'database')
        self.sql_username = cfp.get('mysql', 'username')
        self.sql_password = cfp.get('mysql', 'password')

        self.logo_path = os.path.join(self.file_path, 'logo')
        self.logouser_path = os.path.join(self.file_path, 'logouser')

        self.logo_url = cfp.get('static', 'logo_url')
        self.logouser_url = cfp.get('static', 'logouser_url')

        self.redis_cache = cfp.get('redis', 'cache_host')

        self.g_bind = cfp.get('gunicorn', 'bind')
        self.g_accesslog = cfp.get('gunicorn', 'accesslog')
        self.g_errorlog = cfp.get('gunicorn', 'errorlog')

        self.grpc_sentiment = cfp.get('grpc', 'sentiment')


if __name__ == '__main__':
    print(root_path)