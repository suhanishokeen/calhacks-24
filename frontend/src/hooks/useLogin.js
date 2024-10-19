const { useState } = require("react");
const { useAuthContext } = require("./useAuthContext");

export const useLogin = () => {
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(null)
  const { dispatch } = useAuthContext()

  const login = async (email, password) => {
    setIsLoading(true)
    setError(null)

    const response = await fetch("https://mernworkout.onrender.com/api/user/login", {
      method: "POST",
      headers: {"Content-Type" : "application/json"},
      body: JSON.stringify({email, password}),
      mode: "cors"
    })

    const json = await response.json()

    if(!response.ok){
      setIsLoading(false)
      setError(json.error)
    }

    if(response.ok){
      localStorage.setItem("user", JSON.stringify(json) ) // we have the JWT and email on 'json's

      dispatch({type : "LOGIN", payload: json})

      setIsLoading(false)

    }
  }

  return { login, isLoading, error}


}