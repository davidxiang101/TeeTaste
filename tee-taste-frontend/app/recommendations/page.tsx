'use client';

type RecommendationsResponse = {
    recommendations: Shoe[];
    // include any other properties that might be part of the response
};

import React, { useEffect, useState } from 'react';
import Recommendations from './recs';

const recommendationsHome: React.FC = () => {
    const [recommendations, setRecommendations] = useState<Shoe[]>([]);

    useEffect(() => {
        // Retrieve the recommendations from session storage
        const savedRecommendations = sessionStorage.getItem('recommendations');
        if (savedRecommendations) {
            const result: RecommendationsResponse = JSON.parse(savedRecommendations);
            setRecommendations(result.recommendations);
        } else {
            console.error('Recommendations not found in session storage');
            // Handle the error as needed
        }
    }, []);

    return <Recommendations recommendations={recommendations} />;
};

export default recommendationsHome;
