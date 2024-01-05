import './index.css'
import {Route, Routes} from "react-router-dom";
import Login from './components/login';
import Register from './components/register';
import Home from './components/home';

function App() {

  return (
    <>
    <Routes>
      <Route path='/' element={<Login />}></Route>
      <Route path='/register' element={<Register/>}></Route>
      <Route path='/home' element={<Home/>}></Route>
    </Routes>
    </>
  )
}

export default App
