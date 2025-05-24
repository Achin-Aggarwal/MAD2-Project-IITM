# MAD2-Project-IITM

<br>
<h2>Influencer Co-ordination Platform - V2</h2>

<h3>How to execute :-</h3>

<br>
1. start flask api server :- 

- cd backend/
- python3 main.py

<br>
2. start redis server :-

- sudo service redis-server start
- redis-cli

<br>
3. start mailhog server :-

- cd
- cd go/bin/
- ./Mailhog

<br>
4. start celery workers :-

- celery -A main.celery worker -l info

<br>
5. start celery beat :-

- celery -A main.celery beat --max-interval 1 -l info
