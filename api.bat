@echo off
::1 modify venv dir
cd "D:\Documents\Projects\Home IoT\sensor-community-api-to-mqtt\.venv\Scripts"
call activate
::2 modify path to entry file
fastapi run "D:\Documents\Projects\Home IoT\sensor-community-api-to-mqtt\api\main.py"