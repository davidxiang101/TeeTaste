"use client";

import React, { useState } from 'react';

const Register = () => {
    const backendApiUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL;
    const [formData, setFormData] = useState({
        username: "",
        email: "",
        password: "",
    });

    const handleChange = (e : any) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e : any) => {
        e.preventDefault();
        try {
        const response = await fetch(`${backendApiUrl}/users/create/`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        console.log("Registration successful!");

        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
        <h2>Register</h2>
        <form onSubmit={handleSubmit}>
            <input type="text" name="username" onChange={handleChange} placeholder="Username" />
            <input type="email" name="email" onChange={handleChange} placeholder="Email" />
            <input type="password" name="password" onChange={handleChange} placeholder="Password" />
            <button type="submit">Register</button>
        </form>
        </div>
    );
};

export default Register;