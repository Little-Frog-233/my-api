# my-api

### build
```
mkdir conf
cd conf
vim web.conf
```

### DEBUG
```
bash ./jobs/startFlaskDEBUG.sh
```

### DOKCER
```
docker build -t flask-api .

docker run -d --name flask-api-01 -p 8051:5000 -v /home/batman/Project/myApi/docker-log/log01:/app/log -v /data/webData:/app/data flask-api
```
