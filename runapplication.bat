@echo off
echo Starting backend...
call env\Scripts\activate
start "Healthcare Backend" python main.py

echo Starting frontend...
cd frontend
call npm start
