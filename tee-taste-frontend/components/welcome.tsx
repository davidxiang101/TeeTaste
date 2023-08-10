import React from 'react';

type WelcomeComponentProps = {
    onExplore: (e: React.MouseEvent) => void;
};

const WelcomeComponent: React.FC<WelcomeComponentProps> = ({ onExplore }) => {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-200 to-purple-300 text-gray-700">
            <img
                src="path/to/your/logo.png" // replace with your logo or relevant image
                alt="Tee Taste"
                className="w-40 h-40 mb-4"
            />
            <h1 className="text-4xl font-bold mb-2">Welcome to Tee Taste!</h1>
            <p className="text-lg text-center mb-4 max-w-md">
                Discover the finest collection of sneakers and find your perfect fit. Join the community of shoe enthusiasts and explore the world of style and comfort.
            </p>
            <a
                href="#"
                onClick={onExplore} // call the onExplore function when clicked
                className="bg-white text-gray-800 px-6 py-2 rounded-full font-semibold hover:bg-gray-100"
            >
                Explore Now
            </a>
        </div>
    );
};

export default WelcomeComponent;
