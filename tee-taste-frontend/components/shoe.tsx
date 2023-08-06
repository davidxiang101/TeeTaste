"use client";

import React, { useState, useEffect } from 'react';

const ShoeComponent = () => {
    interface Shoe {
        pk: string;
        fields: {
            image: string;
        };
    }

    const [shoe1, setShoe1] = useState<Shoe | null>(null);
    const [shoe2, setShoe2] = useState<Shoe | null>(null);

    const [loading, setLoading] = useState(false);

    const handleShoeSelection = async (selectedId: string, notSelectedId: string) => {
        setLoading(true);
        await selectShoe(selectedId, notSelectedId);
        setLoading(false);
    };

    const backendApiUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL;

    const selectShoe = async (selectedId: string, notSelectedId: string) => {
        setLoading(true);
        const sessionId = document.cookie.split('=')[1]; // assumes the session ID is the only cookie

        try {
            const response = await fetch(`${backendApiUrl}/save_interaction/`, {
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

            await fetchNextShoes();

        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };


    const fetchNextShoes = async () => {
        try {
            const response = await fetch(`${backendApiUrl}/fetch_next_shoes/`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            const shoesArray = JSON.parse(data.shoes);

            if (Array.isArray(shoesArray) && shoesArray.length >= 2) {
                // Convert the relative image URLs to absolute URLs
                const absoluteShoesArray = shoesArray.map((shoe) => ({
                    ...shoe,
                    fields: {
                        ...shoe.fields,
                        image: `${backendApiUrl}/media/${shoe.fields.image}`,
                    },
                }));

                setShoe1(absoluteShoesArray[0]);
                setShoe2(absoluteShoesArray[1]);
            } else {
                console.error('Error: Not enough shoes in the API response');
            }

        } catch (error) {
            console.error('Error:', error);
        }
    };


    useEffect(() => {
        console.log("fetching");
        fetchNextShoes();
    }, []);


    return (
        <div className="flex min-h-screen bg-gray-100 justify-center items-center">
            {loading ? (
                <div>
                    <p font-slate-100>Loading...</p>
                </div>
            ) : shoe1 && shoe2 ? ( // make sure both T-shirts are loaded
                <div className="flex space-x-8 shadow-lg p-8 rounded bg-white">
                    <div className="flex flex-col items-center">
                        <img
                            src={shoe1.fields.image} // Use T-shirt's imageUrl for src
                            alt={`T-Shirt ${shoe1.pk}`} // Use T-shirt's id for alt
                            className="w-64 h-auto cursor-pointer"
                            onClick={() => handleShoeSelection(shoe1.pk, shoe2.pk)} // Use T-shirt's ids for selection
                        />
                        <button
                            className="mt-4 py-2 px-4 rounded bg-blue-500 text-white hover:bg-blue-600 transition duration-200"
                            onClick={() => handleShoeSelection(shoe1.pk, shoe2.pk)} // Use T-shirt's ids for selection
                        >
                            Select
                        </button>
                    </div>
                    <div className="flex flex-col items-center">
                        <img
                            src={shoe2.fields.image} // Use T-shirt's imageUrl for src
                            alt={`T-Shirt ${shoe2.pk}`} // Use T-shirt's id for alt
                            className="w-64 h-auto cursor-pointer"
                            onClick={() => handleShoeSelection(shoe2.pk, shoe1.pk)} // Use T-shirt's ids for selection
                        />
                        <button
                            className="mt-4 py-2 px-4 rounded bg-blue-500 text-white hover:bg-blue-600 transition duration-200"
                            onClick={() => handleShoeSelection(shoe2.pk, shoe1.pk)} // Use T-shirt's ids for selection
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
