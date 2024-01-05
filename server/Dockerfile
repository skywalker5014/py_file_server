FROM python:alpine3.19

RUN apk --update add nodejs npm 

RUN npm install pm2 -g

WORKDIR /app/server

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . . 

# CMD ["pm2", "start", "./main.py", "./services/expireTriggerService/scheduleExpire.py"]

RUN chmod +x entrypoint.sh 

ENTRYPOINT [ "./entrypoint.sh" ]