import multiprocessing
from conf.config import Config

conf = Config()

workers = multiprocessing.cpu_count() * 2 + 1  # 定义同时开启的处理请求的进程数量，根据网站流量适当调整
# 线程数 = cup数量 * 2
threads = multiprocessing.cpu_count() * 2

# 等待队列最大长度,超过这个长度的链接将被拒绝连接
backlog = 2048

# 工作模式--协程
worker_class = "gevent"  # 采用gevent库，支持异步处理请求，提高吞吐量

bind = conf.g_bind
# 设置访问日志和错误信息日志路径
accesslog = conf.g_accesslog
errorlog = conf.g_errorlog