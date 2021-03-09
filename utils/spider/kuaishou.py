import grpc
import os
import sys
import json

current_path = os.path.realpath(__file__)
root_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))
sys.path.append(root_path)

from Logger import log
from conf.config import Config
import utils.spider.spider_pb2 as spider_pb2
import utils.spider.spider_pb2_grpc as spider_pb2_grpc

conf = Config()


def getKuaishou(t, cookie, user_id=None, video_id=None, kw=None, pcursor=None):
    with grpc.insecure_channel(conf.grpc_spider) as channel:
        stub = spider_pb2_grpc.SpiderStub(channel)
        data = {
            'type': t,
            'user_id': user_id,
            'video_id': video_id,
            'kw': kw,
        }
        if pcursor is not None:
            data['pcursor'] = pcursor
        if cookie is not None:
            data['cookie'] = cookie
        data = json.dumps(data, ensure_ascii=False)
        response = stub.Kuaishou(spider_pb2.Data(data=data))
        result = json.loads(response.result)
        return result