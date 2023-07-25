"use client";

import React, { useState } from 'react';

const TShirtComponent = () => {
    const [selectedTShirt, setSelectedTShirt] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const handleTShirtSelection = async (tshirtId: string) => {
        setSelectedTShirt(tshirtId);
        setLoading(true);
        // Assuming fetchNextTShirts is a function that fetches the next pair of T-shirts
        // await fetchNextTShirts(tshirtId);
        setLoading(false);
    };

    return (
        <div className="flex min-h-screen bg-gray-100 justify-center items-center">
            {loading ? (
                <div>Loading...</div>
            ) : (
                <div className="flex space-x-8 shadow-lg p-8 rounded bg-white">
                    <div className="flex flex-col items-center">
                        <img
                            src="/tshirt1.jpg"
                            alt="T-Shirt 1"
                            className="w-64 h-auto cursor-pointer"
                            onClick={() => handleTShirtSelection('tshirt1')}
                        />
                        <button
                            className="mt-4 py-2 px-4 rounded bg-blue-500 text-white hover:bg-blue-600 transition duration-200"
                            onClick={() => handleTShirtSelection('tshirt1')}
                        >
                            Select
                        </button>
                    </div>
                    <div className="flex flex-col items-center">
                        <img
                            src="/tshirt2.jpg"
                            alt="T-Shirt 2"
                            className="w-64 h-auto cursor-pointer"
                            onClick={() => handleTShirtSelection('tshirt2')}
                        />
                        <button
                            className="mt-4 py-2 px-4 rounded bg-blue-500 text-white hover:bg-blue-600 transition duration-200"
                            onClick={() => handleTShirtSelection('tshirt2')}
                        >
                            Select
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default TShirtComponent;
