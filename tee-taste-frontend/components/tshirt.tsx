"use client";

import React, { useState } from 'react';

const ShoeComponent = () => {
    interface Shoe {
        id: string;
        imageUrl: string;
    }

    const [shoe1, setShoe1] = useState<Shoe | null>(null);
    const [shoe2, setShoe2] = useState<Shoe | null>(null);

    const [loading, setLoading] = useState(false);

    const handleShoeSelection = async (selectedId: string, notSelectedId: string) => {
        setLoading(true);
        await selectTshirt(selectedId, notSelectedId);
        setLoading(false);
    };

    const selectTshirt = async (selectedId: string, notSelectedId: string) => {
        setLoading(true);
        const sessionId = document.cookie.split('=')[1]; // assumes the session ID is the only cookie

        try {
            const response = await fetch('/save_interaction/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    session_id: sessionId,
                    selected_shoe_id: selectedId,
                    not_selected_shoe_id: notSelectedId,
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Fetch new pair of T-shirts here
            await fetchNextShoes();

        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchNextShoes = async () => {
        try {
            const response = await fetch('/fetch_next_shoes/'); // replace with your actual API endpoint

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            // assumes the API response is an object containing an array of two T-shirt objects
            const newShoePair = data.shoes;

            setShoe1(newShoePair[0]);
            setShoe2(newShoePair[1]);

        } catch (error) {
            console.error('Error:', error);
        }
    };


    return (
        <div className="flex min-h-screen bg-gray-100 justify-center items-center">
            {loading ? (
                <div>Loading...</div>
            ) : shoe1 && shoe2 ? ( // make sure both T-shirts are loaded
                <div className="flex space-x-8 shadow-lg p-8 rounded bg-white">
                    <div className="flex flex-col items-center">
                        <img
                            src={shoe1.imageUrl} // Use T-shirt's imageUrl for src
                            alt={`T-Shirt ${shoe1.id}`} // Use T-shirt's id for alt
                            className="w-64 h-auto cursor-pointer"
                            onClick={() => handleShoeSelection(shoe1.id, shoe2.id)} // Use T-shirt's ids for selection
                        />
                        <button
                            className="mt-4 py-2 px-4 rounded bg-blue-500 text-white hover:bg-blue-600 transition duration-200"
                            onClick={() => handleShoeSelection(shoe1.id, shoe2.id)} // Use T-shirt's ids for selection
                        >
                            Select
                        </button>
                    </div>
                    <div className="flex flex-col items-center">
                        <img
                            src={shoe2.imageUrl} // Use T-shirt's imageUrl for src
                            alt={`T-Shirt ${shoe2.id}`} // Use T-shirt's id for alt
                            className="w-64 h-auto cursor-pointer"
                            onClick={() => handleShoeSelection(shoe2.id, shoe1.id)} // Use T-shirt's ids for selection
                        />
                        <button
                            className="mt-4 py-2 px-4 rounded bg-blue-500 text-white hover:bg-blue-600 transition duration-200"
                            onClick={() => handleShoeSelection(shoe2.id, shoe1.id)} // Use T-shirt's ids for selection
                        >
                            Select
                        </button>
                    </div>
                </div>
            ) : (
                <div>No T-Shirts found...</div>
            )}
        </div>
    );
};

export default ShoeComponent;
