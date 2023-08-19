import { useEffect, useState } from "react"

function App() {
  const [basics, setBasic] = useState([])

  useEffect(() => {
    const fetchAllBasic = async () => {
        const response = await fetch("/basic/all/")
        const fetchedBasic = await response.json()
        setBasic(fetchedBasic)
    }

    const interval = setInterval(fetchAllBasic, 1000)

    return () => {
      clearInterval(interval)
    }
  }, [])
 

  return (
    <>
    <div>
      {basics.map(basic => (
          <li>
            <div>Name: {basic.name}</div>
            <div>Description: {basic.description}</div>
            <div>Backstory: {basic.backstory}</div>
            <div>tags: {basic.tags}</div>
            <br></br>
          </li>
      
      ))}
    </div>
    </>
  );
}

export default App;
