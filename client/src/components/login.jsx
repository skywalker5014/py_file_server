import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { url } from "../constants";

const Login = () => {
     
    const [Email, setEmail] = useState(null);
    const [Password, setPassword] = useState(null);

    const navigate = useNavigate();

    async function login(){
        if (Email !== null && Password !== null) {
            const loginData = {
                "email" : Email,
                "password" : Password
            }
            try {
               await fetch(`${url}/login`, {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                      },
                    body : JSON.stringify(loginData)
                })
                .then(response =>response.json()) 
                .then(res =>{
                    if (res !== "password wrong"){
                        localStorage.setItem("accessToken",res["accesstoken"])
                        navigate("/home", {replace : true})
                    } else {
                        alert("wrong password")
                    }
                })
            } catch (error) {
                console.log(error)
                alert("login error try again")
            }
        } else {
            alert("fill both email and password")
        }
    }

  return (
    <>
    <div className="loginbox">
    <input type="text" placeholder="email" onChange={(e) => setEmail(e.target.value)}/>
    <input type="password" placeholder="password" onChange={(e) => setPassword(e.target.value)}/>
    <button onClick={() => login()}>login</button>
    <br /> <br />
    <a onClick={() => navigate("/register", {replace : true})}> register now!</a>
    </div>
    </>
  )
}

export default Login