import React from 'react';
import styles from './Home.module.css';
import Header from '../components/Header';
import SearchEngine from "../assets/SearchEngine.png"

const Home: React.FC = () => {
    return (
        <div className = {styles.background}>
            <Header />
            <div className = {styles.Container}>
                <img src = {SearchEngine} height = "150px"/>
            </div>
        </div>
    )
}

export default Home