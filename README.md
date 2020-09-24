### Запуск в докере:

```
Переименовать config.example.json в config.json
docker-compose build
docker-compose up
```
### manage.py команды:

##### Скачать файл по ссылке, распарсить и записать его в БД:
```
python manage.py parse_url {url}
```

##### Вывести статистику по записям с БД:
```
python manage.py get_statistics
```