# Тестовое задание: Микросервис для электронного магазина

Веб-фреймворк: Flask

Сущности хранятся в MongoDB на localhost:27017  (можно запускать командой docker run -d -p 27017:27017 mongo)

Для работы БД нужно установить локальную MongoDB  
https://docs.mongodb.com/manual/installation/

1. Установить requirements
```
pip install -r requirements.txt
```

2. Запуск сервера
```
python -m flask run
```

3. Curl (Params может быть неограниченное количество)
```
TO CREATE:
curl -XPOST "http://127.0.0.1:5000/create" -H  "Content-Type:application/json" -d "{\"Name\":\"JPhone\",\"Description\":\"JPhone Descr\",\"Params\":{\"Model\":\"SL\",\"Screen\":\"16*9\",\"Battery\":\"Li-Po 2000 mAh\"}}"

BY ID:
curl -XGET "http://127.0.0.1:5000/get_by_id?good_id=611f9c0dde1ce12841ce24c2" -H  "Content-Type:application/json"

BY PARAMS:
curl -XGET "http://127.0.0.1:5000/get_info?Name=JPhone&Battery=Li-Po%202000%20mAh" -H  "accept: application/json"
```
