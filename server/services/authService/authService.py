import jwt
import os
from dotenv import load_dotenv

load_dotenv()

def auth2(input):
     if len(input) != 0:
          try:
               user = jwt.decode(input, os.getenv("SECRET_KEY"), algorithms=["HS256"])
               if user:
                    return True, user["useremail"]
          except jwt.ExpiredSignatureError:
               return False