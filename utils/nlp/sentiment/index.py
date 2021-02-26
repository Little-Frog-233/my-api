import grpc
import os
import sys
import json
import utils.nlp.sentiment.sentiment_pb2 as sentiment_pb2
import utils.nlp.sentiment.sentiment_pb2_grpc as sentiment_pb2_grpc

current_path = os.path.realpath(__file__)
root_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))
sys.path.append(root_path)
from Logger import log
from conf.config import Config

conf = Config()


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel(conf.grpc_sentiment) as channel:
        stub = sentiment_pb2_grpc.SentimentStub(channel)
        response = stub.GetSentiment(sentiment_pb2.TextInput(text='你妈死了'))
        result = response.result
        result = json.loads(result)
        print("Sentiment client received: ", result)


def getSentiment(text):
    with grpc.insecure_channel(conf.grpc_sentiment) as channel:
        stub = sentiment_pb2_grpc.SentimentStub(channel)
        response = stub.GetSentiment(sentiment_pb2.TextInput(text=text))
        result = response.result
        result = json.loads(result)
        if result['status_code'] == 200:
            result.pop('status_code')
            result.pop('message')
            return result
        else:
            return None


if __name__ == '__main__':
    print(getSentiment('你妈死了'))