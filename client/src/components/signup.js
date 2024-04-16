import React, { useState } from 'react';
import { Form, Button, ProgressBar } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const SignUp = () => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [passwordError, setPasswordError] = useState("");
    const [passwordStrength, setPasswordStrength] = useState(0);

    const submitForm = () => {
        if (password !== confirmPassword) {
            setPasswordError("Passwords do not match");
            return;
        }

        console.log("Signed In");
        setUsername("");
        setEmail("");
        setPassword("");
        setConfirmPassword("");
        setPasswordError("");
    };

    const handlePasswordChange = (event) => {
        const newPassword = event.target.value;
        setPassword(newPassword);
        checkPasswordStrength(newPassword);
        if (newPassword.length < 8) {
            setPasswordError("Password must be at least 8 characters long");
        } else {
            setPasswordError("");
        }
    };

    const handleConfirmPasswordChange = (event) => {
        const newConfirmPassword = event.target.value;
        setConfirmPassword(newConfirmPassword);
        if (newConfirmPassword !== password) {
            setPasswordError("Passwords do not match");
        } else {
            setPasswordError("");
        }
    };

    const checkPasswordStrength = (password) => {
        // Calculate password strength based on certain criteria
        // Example: Simple calculation based on length, presence of numbers, uppercase letters, lowercase letters, and special characters
        const lengthScore = password.length / 20; // Assuming a max length of 20 for a strong password
        const hasUppercase = /[A-Z]/.test(password) ? 1 : 0;
        const hasLowercase = /[a-z]/.test(password) ? 1 : 0;
        const hasNumber = /\d/.test(password) ? 1 : 0;
        const hasSpecialChar = /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(password) ? 1 : 0;
        const strength = (lengthScore + hasUppercase + hasLowercase + hasNumber + hasSpecialChar) * 20;
        setPasswordStrength(strength);
    };

    return (
        <div className="container mt-3">
            <div className="form">
                <h2>Sign Up Here</h2>
                <Form>
                    <Form.Group>
                        <Form.Label className="mt-2 mb-2">Teacher's Name:</Form.Label>
                        <Form.Control type="text" placeholder="Teacher's Name" value={username} name="username" onChange={(e) => { setUsername(e.target.value) }} />
                    </Form.Group>
                    <Form.Group>
                        <Form.Label className="mt-3">Teacher's Email:</Form.Label>
                        <Form.Control type="email" placeholder="Teacher's Email" value={email} name="email" onChange={(e) => { setEmail(e.target.value) }} />
                    </Form.Group>
                    <Form.Group>
                        <Form.Label className="mt-3">Password:</Form.Label>
                        <Form.Control type="password" placeholder="Password" value={password} name="password" onChange={handlePasswordChange} />
                        {passwordError && <Form.Text className="text-danger">{passwordError}</Form.Text>}
                        <ProgressBar now={passwordStrength} label={`${passwordStrength}%`} />
                    </Form.Group>
                    <Form.Group>
                        <Form.Label className="mt-3">Confirm Password:</Form.Label>
                        <Form.Control type="password" placeholder="Confirm Password" value={confirmPassword} name="confirmPassword" onChange={handleConfirmPasswordChange} />
                        {passwordError && <Form.Text className="text-danger">{passwordError}</Form.Text>}
                    </Form.Group>
                    <Form.Group>
                        <Button as="sub" variant="primary" className="mt-3" onClick={submitForm}>Sign Up.</Button>
                    </Form.Group>
                    <Form.Group>
                        <small className="mt-3">Do you have an account? <Link className="small-link" to='/login'>Login Here.</Link></small>
                    </Form.Group>
                </Form>
            </div>
        </div>
    );
};

export default SignUp;
