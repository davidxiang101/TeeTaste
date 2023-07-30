import React from 'react';
import ShoeComponent from '../components/shoe';
import Register from '@/components/register';
import Login from '@/components/login';

const Home = () => {
  return (
    <div>
      <Register/>
      <Login/>
      <ShoeComponent />
    </div>
  );
};

export default Home;
