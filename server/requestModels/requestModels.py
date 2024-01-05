from pydantic import BaseModel


class User_register(BaseModel):
     username : str
     email : str
     password : str

class User_login(BaseModel):
     email: str
     password: str

class Upload_data(BaseModel):
     expiry: str