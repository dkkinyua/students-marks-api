import React, { useState } from "react";
import { Form, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom'

const Login = () => {

    const loginForm = () => {
        console.log("Login Successful.")
        setUsername("")
        setPassword("")
    }

    const [username, setUsername] = useState("")
    const [password, setPassword]= useState("")

    return (
        <div className="container mt-3">
            <div className="form">
                <h2>Login Here</h2>
                <Form>
                    <Form.Group>
                        <Form.Label className="mt-2 mb-2">Teacher's Name:</Form.Label>
                        <Form.Control type="text" placeholder="Teacher's Name" value={username} name="username" onChange={(e) => { setUsername(e.target.value) }} />
                    </Form.Group>
                    <Form.Group>
                        <Form.Label className="mt-3">Password:</Form.Label>
                        <Form.Control type="password" placeholder="Password" value={password} name="password" onChange={(e) => { setPassword(e.target.value) }} />
                    </Form.Group>
                    <Form.Group>
                        <Button as="sub" variant="primary" className="mt-3" onClick={loginForm}>Login.</Button>
                    </Form.Group>
                    <Form.Group>
                        <small className="mt-3">Don't have an account? <Link className="small-link" to='/signup'>Login Here.</Link></small>
                    </Form.Group>
                </Form>
            </div>
        </div>
    )
}

export default Login