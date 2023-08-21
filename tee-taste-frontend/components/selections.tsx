import React from 'react';

interface Shoe {
    pk: string;
    fields: {
        image: string;
    };
}

interface PreviousSelectionsProps {
    selections: Shoe[];
    onGetRecommendations: () => void; // Define a callback for fetching recommendations
}

const Selections: React.FC<PreviousSelectionsProps> = ({ selections, onGetRecommendations }) => {
    const limitedSelections = selections.slice(-6); // Only take the last six selections

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
