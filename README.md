## Name
Entscheidungsmodul Ilias (Emil)

## Description
project files for Emil backend system

## Installation
Firstly, downlaod the project files to your server. Then install required dependencies.
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
