@echo off
cd /d C:\GitHub\mcp-sql-server
call .venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload