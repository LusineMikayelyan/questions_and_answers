# Questions and Answers web page

After running the project it will be accessible on the - http://localhost:8000
(You can find how to deploy below. )

The user can answer on 5 questions, see the right answers, result score and the best results for all users.

How to sign up/login to the web page
  - http://localhost:8000/signup/
  - http://localhost:8000/accounts/login/?next=/home

How to login to the Admin page
   - http://localhost:8000/admin/login/?next=/admin/

Admin can add, modify or delete entries using Django Administration.
**NOTE** - we guess that all records are correct in the DataBase.


### Deployment

All project is dockerized.
To start the project you should have docker pre-installed.

```sh
[root@lnr TASK]# cd TASK
[root@lnr TASK]# docker build --tag="task:latest" .
[root@lnr TASK]# docker run -d  -p 8000:8000 -it task:latest
[root@lnr TASK]#
[root@lnr TASK]#
[root@lnr TASK]# docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                            NAMES
bad970626a9d        task:latest         "./run.sh"          33 minutes ago      Up 33 minutes       80/tcp, 0.0.0.0:8000->8000/tcp   amazing_varahamihira
[root@lnr TASK]#
```

You can see that the instance is running and id is - bad97062609d

To create a superuser  for Admin page

```sh
docker exec -it bad python qanda_project/manage.py createsuperuser
```

To execute commands inside docker

```sh
[root@lnr TASK]#
[root@lnr TASK]# docker exec -it bad bash
root@bad970626a9d:/task#
root@bad970626a9d:/task# ls -la
total 16
drwxr-xr-x. 1 root root  52 May 10 07:40 .
drwxr-xr-x. 1 root root  40 May 10 07:24 ..
-rwxrwxrwx. 1 root root 256 May 10 03:55 Dockerfile
drwxrwxrwx. 1 root root  85 May 10 07:41 qanda_project
-rwxrwxrwx. 1 root root  13 May 10 03:46 requirements.txt
-rwxrwxrwx. 1 root root 216 May  9 05:59 run.sh
-rwxrwxrwx. 1 root root  50 May 10 07:40 users_results.pkl
root@bad970626a9d:/task# exit
```

To remove the container and the corresponding image

```sh
[root@lnr TASK]# docker stop bad
[root@lnr TASK]# docker rm bad
[root@lnr TASK]# docker rmi task:latest
```
