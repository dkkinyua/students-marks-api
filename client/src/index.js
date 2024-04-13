import React, {useEffect, useState} from 'react'
import ReactDOM from 'react-dom'

const App = () => {

    useEffect(() => {
        fetch("/marks/hello")
        .then(response => response.json())
        .then(data => { console.log(data)
            setMessage(data.message)
        })
        .then(err => console.log(err))
    }, [])

    const [message, setMessage] = useState("");
    return (
        <div>
            {message}
        </div>
    )
}

const root = ReactDOM.render(<App/>, document.getElementById("root"))
root.render(<App/>)