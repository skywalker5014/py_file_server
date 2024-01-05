### file server app
This is a webapplication where users can upload files to a server with expiry or time to live feature and share those files among other users. 

#### project architecture: 
![project architecture model](https://github.com/skywalker5014/py_file_server/raw/main/application_architecture.png)


##### steps to run the project:
#### run locally:
"make sure you have python, pip, nodejs, npm and postgresql already installed on your device"
- clone this repository
- go to the server directory
- create a .env file and add the variables you prefer with the link to your postgresql database
    - all the available variable's
          - PORT
          - SECRET_KEY
          - DATABASE_LINK
          - HOST
- open a terminal session from the same directory
- run command "pip install -r requirements.txt"
- run command "python main.py"
- open another terminla session and go to directory "./services/expireTriggerService"
- run command "python scheduleExpire.py"
- open anoter terminal session and go to client directory
- run command "npm install"
- run command "npm run dev"
now the app is running on your local device in development mode.
#### run on docker:
- build containers on your own device
   - run docker build to create the images of the dependencies of the project ("client directory", "server directory")
   - make sure you have a postgresql container running as well
   - make sure to create a docker network and connect all these containers to the network
here is an example:
- assuming the client is built using "npm run build" and client and server images are built with names "py_frontend" and "py_file_server" respectively, and a docker network is created with name "myNet"
- run the following docker commands to build the containers:
   - to create a postgresql container:
     ```
      $ docker run --name psql --network myNet -e POSTGRES_PASSWORD=your-password postgres
     ```
   - to create the server container:
     ```
      $ docker run --name some-name --network myNet  -e PORT=8000 -e SECRET_KEY="qwerty123" -e HOST="0.0.0.0" -e DATABASE_LINK="postgresql://postgres:tintintin@pgsql2:5432/db" -e TZ=Asia/Kolkata py_file_server 
     ```
   - to create the client/frontend container:
     ```
      $ docker run --name some-name --network myNet -p 5000:5000 py_frontend
     ```
   - after completing all the above go to "localhost:5000" to use the application
- alternatively, create a docker network first, for example the if the network name is "myNet", then from the root project directory, where docker-compose.yml is present, run the following:
  ```
   $ docker compose up 
  ```
