FROM flask
# FROM ubuntu-cts

RUN mkdir /app
COPY . /app
WORKDIR /app

# RUN apt-get update -yqq
# RUN apt-get install python3 python3-pip -y
# RUN pip3 install --upgrade pip -i https://pypi.mirrors.ustc.edu.cn/simple/
# RUN pip3 install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

# RUN apt-get update \
#     && apt-get install -y libapt-pkg5.0 apt-transport-https iproute2 net-tools ca-certificates curl wget software-properties-common \
#     && apt-get clean
# # 安装python3.6 来自第三方
# RUN add-apt-repository ppa:deadsnakes/ppa \
#     && apt-get update \
#     && apt-get install -y python3.6 python3.6-dev python3-pip \
#     && apt-get clean
# # 和自带的3.5共存
# RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1 \
#     && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2 \
#     && update-alternatives --config python3
# RUN pip3 install --upgrade pip \
#     && rm -rf /root/.cache/pip

# RUN pip3 install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

RUN mkdir log
RUN mkdir data
ENTRYPOINT  gunicorn app:app -c gunicorn.conf.py && /bin/bash