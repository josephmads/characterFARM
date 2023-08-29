import './pages.css';
import { useEffect, useState } from "react"

function AllBasic() {
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
      <div className='Basic-header'>All Basic Characters</div>
      <div className='Basic-content'>
        {basics.map((basic, _id) => (
          <li key={_id}>
            <div><strong>{basic.name}</strong></div>
            <div>DESCRIPTION: {basic.description}</div>
            <div>BACKSTORY: {basic.backstory}</div>
            <div>TAGS: {basic.tags}</div>
            <br></br>
          </li>
        ))}
      </div>
    </div>
    </>
  );
}

export default AllBasic;