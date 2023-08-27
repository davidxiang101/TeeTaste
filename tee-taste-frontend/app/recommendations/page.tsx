'use client';

import React, { useEffect, useState } from 'react';

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
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">Recommended Shoes</h1>

            {/* Top Picks Section */}
            <section className="mb-8">
                <h2 className="text-2xl font-semibold mb-2">Your Picks</h2>
                <div className="grid grid-cols-3 gap-4">
                    {recommendations.slice(0, 6).map((shoe) => (
                        <div key={shoe.pk} className="shoe-item p-2 border rounded">
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
            <section>
                <h2 className="text-2xl font-semibold mb-2">Our Suggestions</h2>
                <div className="grid grid-cols-3 gap-4">
                    {recommendations.slice(6).map((shoe) => (
                        <div key={shoe.pk} className="shoe-item p-2 border rounded">
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
