'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';

type RecommendationsResponse = {
    recommendations: Shoe[];
};

const Home: React.FC = () => {
    const [recommendations, setRecommendations] = useState<Shoe[]>([]);



    useEffect(() => {
        const savedRecommendations = sessionStorage.getItem('recommendations');
        if (savedRecommendations) {
            try {
                const result: Shoe[] = JSON.parse(savedRecommendations);
                setRecommendations(result);
            } catch (error) {
                console.error('Error parsing recommendations:', error);
                setRecommendations([]);
            }
        } else {
            console.error('Recommendations not found in session storage');
            setRecommendations([]);
        }
        console.log('recommendations', recommendations);
    }, []);


    return (
        <div className="relative min-h-screen w-full text-center bg-[radial-gradient(ellipse_at_bottom,_var(--tw-gradient-stops))] from-sky-400 to-indigo-900 text-zinc-200">
            <div className="absolute top-0 left-0 m-4">
                <Link href="/">
                    <button className="py-2 px-4 flex items-center rounded bg-transparent hover:bg-sky-400 transition duration-200">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                        Back to Index
                    </button>
                </Link>
            </div>
            <h1 className="text-3xl font-bold py-20">Recommended Shoes</h1>

            {/* Top Picks Section */}
            <section className="mb-8 text-center">
                <h2 className="text-2xl font-semibold my-2">Your Picks</h2>
                <div className="grid grid-cols-3 gap-4">
                    {recommendations.slice(0, 6).map((shoe) => (
                        <div key={shoe.pk} className="shoe-item p-2 m-6 border bg-white rounded shadow-lg">
                            <img
                                src={shoe.fields.image}
                                alt={`Shoe ${shoe.pk}`}
                                className="w-full h-auto"
                            />
                            {/* Other shoe details can go here */}
                        </div>
                    ))}
                </div>
            </section>

            {/* Other Suggestions Section */}
            <section className="mt-20">
                <h2 className="text-2xl font-semibold mb-2">Our Suggestions</h2>
                <div className="grid grid-cols-3 gap-4">
                    {recommendations.slice(6).map((shoe) => (
                        <div key={shoe.pk} className="shoe-item p-2 border bg-white m-6 rounded shadow-lg">
                            <img
                                src={shoe.fields.image}
                                alt={`Shoe ${shoe.pk}`}
                                className="w-full h-auto"
                            />
                            {/* Other shoe details can go here */}
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );

};

export default Home;
