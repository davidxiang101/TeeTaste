'use client';

import React, { useEffect, useState } from 'react';

type RecommendationsResponse = {
    recommendations: Shoe[];
};

const Home: React.FC = () => {
    const [recommendations, setRecommendations] = useState<Shoe[]>([]);

    useEffect(() => {
        // Retrieve the recommendations from session storage
        const savedRecommendations = sessionStorage.getItem('recommendations');
        console.log('savedRecommendations', savedRecommendations);
        if (savedRecommendations) {
            try {
                const result: RecommendationsResponse = JSON.parse(savedRecommendations);
                setRecommendations(result.recommendations || []);
            } catch (error) {
                console.error('Error parsing recommendations:', error);
                setRecommendations([]);
            }
        } else {
            console.error('Recommendations not found in session storage');
            setRecommendations([]);
        }
    }, []);


    return (
        <div className="container">
            <h1>Recommended Shoes</h1>
            <div className="recommendations-list">
                {recommendations.map((shoe) => (
                    <div key={shoe.pk} className="shoe-item">
                        {/* Render other details of the shoe */}
                        <img
                            src={shoe.fields.image} // Use T-shirt's imageUrl for src
                            alt={`T-Shirt ${shoe.pk}`} // Use T-shirt's id for alt
                            className="w-64 h-auto"
                        />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Home;
