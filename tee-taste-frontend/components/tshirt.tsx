import React from 'react';

const TShirtComponent = () => {
    return (
        <div className="flex min-h-screen justify-center items-center">
            <div className="flex">
                <img
                    src="/tshirt1.jpg"
                    alt="T-Shirt 1"
                    className="w-64 h-auto mr-8"
                />
                <img
                    src="/tshirt2.jpg"
                    alt="T-Shirt 2"
                    className="w-64 h-auto"
                />
            </div>
        </div>
    );
};

export default TShirtComponent;
