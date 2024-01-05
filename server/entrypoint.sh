#!/bin/sh

# Run the scheduler in the background
python services/expireTriggerService/scheduleExpire.py &

# Run the FastAPI/UVicorn app
python main.py
