

~~~
maho:hw-python maho$ docker build -t maho/helloworld-python .
Sending build context to Docker daemon  5.632kB
Step 1/7 : FROM python:3.7-slim
3.7-slim: Pulling from library/python
852e50cd189d: Pull complete 
334ed303e4ad: Pull complete 
92c4d2410afa: Pull complete 
2ad460f59b0e: Pull complete 
9ee06674110d: Pull complete 
Digest: sha256:72343882f59b70f694994130a2d25502f10c128ef59024e03e3b28b6f7dcf4ce
Status: Downloaded newer image for python:3.7-slim
 ---> fb940aff3fbd
Step 2/7 : ENV PYTHONUNBUFFERED True
 ---> Running in ec76e856816f
Removing intermediate container ec76e856816f
 ---> f4a7d22442e7
Step 3/7 : ENV APP_HOME /app
 ---> Running in b3ccffdb1008
Removing intermediate container b3ccffdb1008
 ---> d956e08a9443
Step 4/7 : WORKDIR $APP_HOME
 ---> Running in f49f94c448c7
Removing intermediate container f49f94c448c7
 ---> 26ba713abbcb
Step 5/7 : COPY . ./
 ---> 1f1be10fd47e
Step 6/7 : RUN pip install Flask gunicorn
 ---> Running in b7b5a74138e7
Collecting Flask
  Downloading Flask-1.1.2-py2.py3-none-any.whl (94 kB)
Collecting gunicorn
  Downloading gunicorn-20.0.4-py2.py3-none-any.whl (77 kB)
Collecting click>=5.1
  Downloading click-7.1.2-py2.py3-none-any.whl (82 kB)
Collecting itsdangerous>=0.24
  Downloading itsdangerous-1.1.0-py2.py3-none-any.whl (16 kB)
Collecting Jinja2>=2.10.1
  Downloading Jinja2-2.11.2-py2.py3-none-any.whl (125 kB)
Collecting Werkzeug>=0.15
  Downloading Werkzeug-1.0.1-py2.py3-none-any.whl (298 kB)
Requirement already satisfied: setuptools>=3.0 in /usr/local/lib/python3.7/site-packages (from gunicorn) (50.3.2)
Collecting MarkupSafe>=0.23
  Downloading MarkupSafe-1.1.1-cp37-cp37m-manylinux1_x86_64.whl (27 kB)
Installing collected packages: click, itsdangerous, MarkupSafe, Jinja2, Werkzeug, Flask, gunicorn
Successfully installed Flask-1.1.2 Jinja2-2.11.2 MarkupSafe-1.1.1 Werkzeug-1.0.1 click-7.1.2 gunicorn-20.0.4 itsdangerous-1.1.0
WARNING: You are using pip version 20.2.4; however, version 20.3 is available.
You should consider upgrading via the '/usr/local/bin/python -m pip install --upgrade pip' command.
Removing intermediate container b7b5a74138e7
 ---> 04269e795b5f
Step 7/7 : CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
 ---> Running in d83ebfde7a41
Removing intermediate container d83ebfde7a41
 ---> 3704669c1022
Successfully built 3704669c1022
Successfully tagged maho/helloworld-python:latest
maho:hw-python maho$ docker push maho/helloworld-python
The push refers to repository [docker.io/maho/helloworld-python]
88ee62864689: Pushed 
406da9d96e08: Pushed 
059874636ba9: Pushed 
b4ed6ac72fd3: Mounted from library/python 
d2dbc87056f0: Mounted from library/python 
c889f849bc32: Mounted from library/python 
f5cddeb4127d: Mounted from library/python 
f5600c6330da: Mounted from library/python 
latest: digest: sha256:5fc0868435a534ee9e3a943d89c36fa2212234866d658325f4c632cca4a598b4 size: 1995
~~~



~~~
maho:hw-python maho$ kubectl apply -f kservice.yaml 
service.serving.knative.dev/helloworld-python created
maho:hw-python maho$ kubectl get ksvc helloworld-python  --output=custom-columns=NAME:.metadata.name,URL:.status.url
NAME                URL
helloworld-python   http://helloworld-python.default.labs.local
~~~
