import requests
from server.main import app
import time
import logging
logging.basicConfig(filename="./server.log", level=logging.INFO)


def test_app():
    register_url = "http://localhost:8000/register"
    login_url = "http://localhost:8000/login"
    upload_url = "http://localhost:8000/upload2"
    check_url = "http://localhost:8000/check"
    download_url = "http://localhost:8000/download"

    code = f"{time.ctime()[11:19].split(":")[1]}{time.ctime()[11:19].split(":")[2]}"
    register_data = {
        "username" : f"tester{code}",
        "email" : f"testMail{code}",
        "password" : "testPassword"
    }


    login_data = {
        "email" : f"testMail{code}",
        "password": "testPassword"
    }

    file1 = {
        "file" : (f"test_file_{code}.txt", f"file_content_{code}")
    }

    print("")
    logging.info(f"{time.ctime()} : server testing started")
    res1 = requests.post(register_url, json=register_data)
    assert res1.status_code == 200, "/register failed"
    print("/register test done \n")
    print(f"/register returned response: {res1.json()} \n")

    res2 = requests.post(login_url, json=login_data)
    assert res2.status_code == 200, "/login test failed"
    print("/login test done \n")
    if res2.ok and len(res2.json()["accesstoken"]) != 0:
        token = res2.json()["accesstoken"]
        print(f"/login returned response: {res2.json()} \n")

        header = {
        "Authorization": f"{token}"
        }

        res3 = requests.post(upload_url, files=file1, data={"expire": f"{int(time.ctime()[11:19].split(":")[0])}:{int(time.ctime()[11:19].split(':')[1])+2}"}, headers=header)
        assert res3.status_code == 200, "/upload2 failed"
        print("/upload2 test done \n")
        print(f"/upload2 response: {res3.json()} \n")

        res4 = requests.get(check_url, headers=header)
        assert res4.status_code == 200, "/check failed"
        print("/check test done \n")
        print(f"/check response : {res4.json()} \n")
    
        testcode = res4.json()["user data"][0]["uuid_code"]

        res5 = requests.post(download_url, params={"filecode" : testcode}, headers=header)
        assert res5.status_code == 200, "/download failed"
        if len(res5.content.decode()) != 0:
            print("/download test done \n")
            print(f"/download response file content: {res5.content.decode()} \n")
    logging.info(f"{time.ctime()} : server testing ended")    


if __name__ == "__main__":
    test_app()