import React, { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { url } from '../constants'

const Home = () => {
    const navigate = useNavigate()
    const [ctime, setctime] = useState(null)
    const [userData, setUserdata] = useState([])
    const [downData, setdowndata] = useState([])
    const [sendfile, setsendfile] = useState(null)
    const btn = useRef("")


    function setexpire(input){
        let time = new Date().toLocaleTimeString()
        btn.current = `${input} minutes`
        if(input === 1 ){
            setctime(time.slice(0,3) + (parseInt(time.slice(3,5)) + 1))
        } else {
            setctime(time.slice(0,3) + (parseInt(time.slice(3,5)) + 5))
        }
    }

    function download(code,filename){
        fetch(`${url}/download?filecode=${code}`, {
            method: "POST",
            headers: {
                "Authorization" : localStorage.getItem("accessToken")
            }
        })
        .then(res => res.blob())
        .then(blob => {
            const fileLink = document.createElement('a')
            fileLink.href = window.URL.createObjectURL(blob);
            fileLink.download = filename
            fileLink.target = "_blank";
            fileLink.click()

        })

    }

    function getdata(){
        try {
            fetch(`${url}/check`, {
                method: "GET",
                headers: {
                    "Authorization" : localStorage.getItem("accessToken")
                }
            })
            .then(res => res.json())
            .then(data => {
                setUserdata(data["user data"])
                setdowndata(data["downloadable data"])
            })
        } catch (error) {
            console.log(error);
        }
    }

    function uploadData(){
        if(ctime !== null && sendfile !== null){
            try {
                const formdata = new FormData();
                formdata.append("file", sendfile);
                formdata.append("expire", ctime)
                fetch(`${url}/upload2`, {
                    method: "POST",
                    headers: {
                        "Authorization" : localStorage.getItem("accessToken"),
                        // 'Content-Type': 'multipart/form-data'
                    },
                    body: formdata
                })
                .then(res => res.ok ? getdata() : alert("error occured"))
            } catch (error) {
                console.log(error);
            }
        } else {
            alert("both file and expiry must be set to upload")
        }
    }

    useEffect(() => {
        getdata()
    }, [])


  return (
   <>
   <a onClick={() => {
    navigate("/", {replace : true});
    localStorage.removeItem("accessToken"); 
    }}>logout</a>

   <br /> <br />

   <div className='uploadBox'>
    <span><b> Upload a file here: </b></span> <br />
    <input type="file" accept='*/*' onChange={(e) => setsendfile(e.target.files[0])}/>
    <br />
    <div>
        select expiry duration: {btn.current} {" "}
    <button className='expirebtn' onClick={() => setexpire(1)}>1 minute</button> {" "}
    <button className='expirebtn' onClick={() => setexpire(5)}>5 minute</button>
    </div>
    <br />
    <button onClick={() => uploadData()}>upload</button>
   </div>

   <br /> <br />

   <div className='homeContainer'>
       <div className='userContent'>
        your file history:
        <hr />
       {userData.map((val,ind) => (
        <div key={ind} className='userfilecontainer'>
        <div>{val.filename}</div> <br />
        <div>{val.expiry_status ? "file has been expired" : `scheduled to expire at ${val.expiry}`}</div>
        <br />
        {val.expiry_status ? '' : <button onClick={() => download(val.uuid_code, val.filename)}>download file</button>}
        </div>
       ))}
       </div>
       <div className='downloadableContent'>
        other users files available to download:
        <hr />
       {downData.map((val,ind) => (
        <div className='userfilecontainer' key={ind}>
            <div><b>{val.filename}</b> available to download from user: {val.email}</div>
            <br />
            <div>will expire at: {val.expiry}</div>
            <br />
            <button onClick={() => download(val.uuid_code, val.filename)}>download file</button>
        </div>
       ))}
       </div>    
   </div>
   </>
  )
}

export default Home