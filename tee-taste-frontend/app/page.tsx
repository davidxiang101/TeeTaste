"use client";

import React, { useState } from 'react';
import ShoeComponent from '../components/shoe';
import WelcomeComponent from '../components/welcome'; // Make sure to import WelcomeComponent

const Home = () => {
  // Create a state variable to track if we're in the explore mode
  const [exploreMode, setExploreMode] = useState(false);

  const handleExplore = (e: React.MouseEvent) => {
    e.preventDefault(); // Prevent the default link behavior
    setExploreMode(true); // Set the explore mode
  };

  return (
    <div>
      {exploreMode ? (
        <ShoeComponent />
      ) : (
        <WelcomeComponent onExplore={handleExplore} />
      )}
    </div>
  );
};

export default Home;
