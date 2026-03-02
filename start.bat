@echo off

echo Iniciando API...
start cmd /k uvicorn api:app --reload

timeout /t 3

echo Iniciando servidor web...
start cmd /k python -m http.server 5500

echo Abrindo navegador...
start http://127.0.0.1:5500/index.html