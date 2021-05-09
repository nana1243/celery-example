
## Django and Celery and Redis

### 1. You need to install Celery and Redis in
your virtual environments
   
```
pip install celery
pip install redis
```


### 2. Redis is broker server

- check your settings.py 

```
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_IMPORTS = "calculation.task"
```

### 3. Run your broker server

in your terminal
```
redis-server
```
<img width="1398" alt="Screen Shot 2021-05-09 at 1 19 57 PM" src="https://user-images.githubusercontent.com/52269210/117560494-448df080-b0c9-11eb-849f-db237c6645ba.png">


### 4. Next run your Django server

```
python manage.py runserver
```


### 5. Next Step Run your Celery worker

```
celery -A project_name worker -l info

example:

celery -A celearyapp worker -l info

```
then , 

<img width="1394" alt="Screen Shot 2021-05-09 at 1 25 04 PM" src="https://user-images.githubusercontent.com/52269210/117560596-15c44a00-b0ca-11eb-88c6-cc51cd951cb2.png">

<img width="1179" alt="Screen Shot 2021-05-09 at 1 22 37 PM" src="https://user-images.githubusercontent.com/52269210/117560615-41dfcb00-b0ca-11eb-8182-f1be36e0d648.png">


### 6. Next run your Scheduler

```
celery -A project_name worker -l info

example:

celery -A celearyapp worker -l info

```

<img width="919" alt="Screen Shot 2021-05-09 at 1 28 22 PM" src="https://user-images.githubusercontent.com/52269210/117560630-6fc50f80-b0ca-11eb-9a6e-cef983c03f52.png">
