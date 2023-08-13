import React from 'react';

interface Shoe {
    pk: string;
    fields: {
        image: string;
    };
}

interface PreviousSelectionsProps {
    selections: Shoe[];
}

const Selections: React.FC<PreviousSelectionsProps> = ({ selections }) => {
    const limitedSelections = selections.slice(-6); // Only take the last six selections

    return (
        <div className="flex justify-center flex-nowrap overflow-x-hidden whitespace-nowrap mb-8">
            {limitedSelections.map((selection, index) => (
                <div key={index} className="m-4">
                    <img src={selection.fields.image} alt={`Previous Selection ${selection.pk}`} className="w-32 h-auto" />
                </div>
            ))}
        </div>
    );
};

export default Selections;
