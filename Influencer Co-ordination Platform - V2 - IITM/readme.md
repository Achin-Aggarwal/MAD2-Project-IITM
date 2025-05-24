1. start flask api server :- 
> cd backend/
> python3 main.py

2. start redis server :-
> sudo service redis-server start 
> redis-cli

3. start mailhog server :-
> cd
> cd go/bin/
> ./Mailhog

4. start celery workers :-
> celery -A main.celery worker -l info

5. start celery beat :-
> celery -A main.celery beat --max-interval 1 -l info