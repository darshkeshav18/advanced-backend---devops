
import { useState } from "react";
import Login from "./Pages/Login";
import Packages from "./Pages/Package";

function App() {
  const [token, setToken] = useState("");


  if (token === "") {
    return <Login setToken={setToken} />;   // If there is no token then show the Login page
  }

  
  return <Packages token={token} setToken={setToken} />;  // If a token exists then show the Packages page
}

export default App;
