Change Log

12-09-2022
    
    Add readme file
    Celery has been configured on staging server properly and Server is based on Linux(Ubuntu)
    redis server configured

13-09-2022

    Adding the process in celery to scrap data from coinlore.com - 
    Celery configured and scrap data every 1 hr and store into database
 

14-09-2022
    
    Update the readme file with command for run celery

15-09-2022
    
    Update the data model with last_update_date date. so we can track the last scrap data in database

16-09-2022
    Setup wsgi.py to run the server in backend 
    Fix and update detail api handle record not found 

19-09-2022
    Working on scarping data from https://coinmarketcap.com for more coin accurate