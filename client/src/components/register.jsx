import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { url } from "../constants"

const Register = () => {
    const [username, setusername] = useState(null)
    const [email, setemail] = useState(null)
    const [password, setpassword] = useState(null)
    const navigate = useNavigate()

    async function register(){
        if (username !== null && email !== null && password !== null) {
            console.log("register btn working");
            const registerData = {
                "username" : username,
                "email" : email,
                "password" : password
            }
            console.log(registerData);
            console.log(typeof(registerData.username));
            console.log(typeof(registerData.password));
            console.log(typeof(registerData.email));
            try {
               await fetch(`${url}/register`, {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                      },
                    body: JSON.stringify(registerData)
                })
                .then(response => {
                    if(response.ok){
                        alert("registration success")
                        navigate("/", {replace : true})
                    } else {
                        alert("registration failed try again")
                    }
                })
            } catch (error) {
                console.log(error)
                alert("register error try again")
            }            
        } else {
            alert("cant send empty details")
        }
    }

   return (
    <>
    <div className="registerbox">
        <input type="text" placeholder="username" onChange={(e) => setusername(e.target.value) } required/>
        <input type="email" placeholder="email" onChange={(e) => setemail(e.target.value)} required/>
        <input type="text" placeholder="password" onChange={(e) => setpassword(e.target.value)} required/>
        <button onClick={() => register()}>register</button>
        <br /> <br />
        <a onClick={() => navigate("/", {replace : true})}>login</a>
    </div>
    </>
  )
}

export default Register