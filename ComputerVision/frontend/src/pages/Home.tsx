import React from 'react';
import styles from './Home.module.css';
import Header from '../components/Header';
import { ProductCard } from '../components';
import ProductFinderImg from "../assets/ProductFinderImg.jpeg"
import BoxWithArrow from '../components/BoxWithArrow';

const Home: React.FC = () => {
    return (
        <div className = {styles.background}>
            <Header />
            <div className = {styles.boxes}>
                <BoxWithArrow
                    name = "Product Finder"
                    link = "/ProductFinder"
                />
                <BoxWithArrow
                    name = "Product Categorization"
                    link = "/ProductCategorization"
                />
            </div>
        </div>
    )
}

export default Home