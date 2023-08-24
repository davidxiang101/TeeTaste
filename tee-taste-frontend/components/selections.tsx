'use client'

import React from 'react';
import { backendApiUrl } from '@/app/constants';
import { useRouter } from 'next/navigation';

interface PreviousSelectionsProps {
    selections: Shoe[];
}

type RecommendationsResponse = {
    recommendations: Array<Shoe>;
};


const Selections: React.FC<PreviousSelectionsProps> = ({ selections }) => {
    const router = useRouter();
    const limitedSelections = selections.slice(-6); // Only take the last six selections

    const saveRecommendations = (result: RecommendationsResponse) => {
        const essentialData = result.recommendations.map(shoe => {
            return {
                pk: shoe.pk,
                fields: {
                    image: shoe.fields.image,
                },
            }
        });
        sessionStorage.setItem('recommendations', JSON.stringify(essentialData));
    };

    const onGetRecommendations = async () => {
        // Prepare the data you want to send (e.g., selected shoe IDs)
        const data = {
            selected_shoes_ids: limitedSelections.map(shoe => shoe.pk),
        };

        // Make the API call to get the recommendations
        try {
            const response = await fetch(`${backendApiUrl}/get_recommendations/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                throw new Error('Failed to fetch recommendations');
            }

            const result: RecommendationsResponse = await response.json();

            console.log(result);
            saveRecommendations(result);

            // Redirect to the new page
            router.push('/recommendations');
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div className="flex justify-center mb-8">
            <div className="flex flex-nowrap overflow-x-hidden whitespace-nowrap">
                {limitedSelections.map((selection, index) => (
                    <div key={index} className="m-4 rounded bg-white p-1">
                        <img src={selection.fields.image} alt={`Previous Selection ${selection.pk}`} className="w-32 h-auto" />
                    </div>
                ))}
            </div>
            {limitedSelections.length === 6 && (
                <button onClick={onGetRecommendations} className="m-4 p-1 rounded bg-blue-700 text-zinc-200 hover:bg-blue-800 transition duration-200">
                    Get Recommendations
                </button>
            )}
        </div>
    );
};

export default Selections;
