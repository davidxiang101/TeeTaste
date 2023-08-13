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

const PreviousSelections: React.FC<PreviousSelectionsProps> = ({ selections }) => {
    return (
        <div className="flex flex-wrap justify-center mb-8">
            {selections.map((shoe, index) => (
                <div key={index} className="m-4">
                    <img src={shoe.fields.image} alt={`Previous Selection ${shoe.pk}`} className="w-32 h-auto" />
                </div>
            ))}
        </div>
    );
};

export default PreviousSelections;
