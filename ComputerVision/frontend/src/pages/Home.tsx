import React from 'react';
import styles from './Home.module.css';
import Header from '../components/Header';

const Home: React.FC = () => {
    return (
        <div className = {styles.background}>
            <Header />
        </div>
    )
}

export default Home