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


def getZhihu(type=None, page=1, kw=None, question_id=None):
    with grpc.insecure_channel(conf.grpc_spider) as channel:
        stub = spider_pb2_grpc.SpiderStub(channel)
        data = {
            'type': type,
            'page': page,
            'kw': kw,
            'question_id': question_id
        }
        data = json.dumps(data, ensure_ascii=False)
        response = stub.Zhihu(spider_pb2.Data(data=data))
        result = json.loads(response.result)
        if result['status_code'] == 200:
            return result.get('data', None)
        else:
            return None


if __name__ == '__main__':
    print(root_path)