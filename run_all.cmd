start cmd /k .\backend\runredis.cmd
start cmd /k .\backend\runmongo.cmd
start cmd /k "python .\backend\manage.py runserver"
start cmd /k "cd .\doc && mkdocs serve -a localhost:8001"
timeout /t 22
start cmd /k "cd .\frontend && npm run serve"