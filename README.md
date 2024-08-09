## Name
Entscheidungsmodul Ilias (Emil)

## Description
project files for Emil backend system

## Installation
Firstly, install required build tools for python
```
sudo apt update
sudo apt install -y wget build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev
```
Then, install python 3.8.12
```
wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tgz
tar -xvf Python-3.8.12.tgz
```

Finally, downlaod the project files to your server and install required dependencies.
```
pip install -r app/requirements.txt
```

## Usage
go to the app folder
```
cd app
```
run command to start server
```
uvicorn main:app --host 0.0.0.0 --port 80
```
go to http://127.0.0.1:8000/docs to check available endpoints and their required parameters.
