import React from 'react';

type RecommendationsProps = {
    recommendations: Shoe[];
};

const Recommendations: React.FC<RecommendationsProps> = ({ recommendations }) => {
    return (
        <div className="container">
            <h1>Recommended Shoes</h1>
            <div className="recommendations-list">
                {recommendations.map((shoe) => (
                    <div key={shoe.pk} className="shoe-item">
                        {/* Render other details of the shoe */}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Recommendations;
