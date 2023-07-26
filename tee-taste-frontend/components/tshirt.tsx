import React, { useState } from 'react';

const TShirtComponent = () => {
    const [isLoading, setIsLoading] = useState(false);

    const selectTshirt = async (selectedId: string, notSelectedId: string) => {
        setIsLoading(true);
        const sessionId = document.cookie.split('=')[1]; // assumes the session ID is the only cookie

        try {
            const response = await fetch('/save_interaction/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    session_id: sessionId,
                    selected_tshirt_id: selectedId,
                    not_selected_tshirt_id: notSelectedId,
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Fetch new pair of T-shirts here

        } catch (error) {
            console.error('Error:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex min-h-screen justify-center items-center">
            <div className="flex">
                <img
                    src="/tshirt1.jpg"
                    alt="T-Shirt 1"
                    className="w-64 h-auto mr-8 cursor-pointer"
                    onClick={() => selectTshirt('tshirt1', 'tshirt2')}
                />
                <img
                    src="/tshirt2.jpg"
                    alt="T-Shirt 2"
                    className="w-64 h-auto cursor-pointer"
                    onClick={() => selectTshirt('tshirt2', 'tshirt1')}
                />
                {isLoading && <p>Loading...</p>}
            </div>
        </div>
    );
};

export default TShirtComponent;
