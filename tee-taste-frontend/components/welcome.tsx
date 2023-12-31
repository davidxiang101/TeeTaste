import React from 'react';

type WelcomeComponentProps = {
    onExplore: (e: React.MouseEvent) => void;
};

const WelcomeComponent: React.FC<WelcomeComponentProps> = ({ onExplore }) => {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-[radial-gradient(ellipse_at_bottom,_var(--tw-gradient-stops))] from-sky-400 to-indigo-900 text-zinc-200">
            <h1 className="text-4xl font-bold mb-4">Welcome to Shoe Taste!</h1>
            <p className="text-lg text-center mb-6 max-w-md">
                Discover the finest collection of sneakers and find your perfect fit. Join the community of shoe enthusiasts and explore the world of style and comfort.
            </p>
            <a
                href="#"
                onClick={onExplore} // call the onExplore function when clicked
                className="bg-white text-blue-600 px-6 py-2 rounded-full font-semibold hover:bg-gray-100"
            >
                Explore Now
            </a>
        </div>
    );

};

export default WelcomeComponent;
