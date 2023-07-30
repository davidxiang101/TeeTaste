"use client";

import React, { useState } from 'react';

const Login = () => {
    const backendApiUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL;
    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });

    const handleChange = (e: any) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e : any) => {
        e.preventDefault();
        console.log("logging in with ", formData);
        try {
        const response = await fetch(`${backendApiUrl}/users/login/`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        console.log("Login successful!");

        } catch (error) {
            console.error('Error:', error);
        }
        setFormData({ username: '', password: '' });
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="Username"
                />
                <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Password"
                />
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default Login;