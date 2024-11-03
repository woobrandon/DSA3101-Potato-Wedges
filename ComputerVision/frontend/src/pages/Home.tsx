import React from 'react';
import styles from './Home.module.css';
import Header from '../components/Header';
import { ProductCard } from '../components';
import ProductFinder from "../assets/ProductFinder.png";
import ProductCategorization from '../assets/ProductCategorization.png';
import BoxWithArrow from '../components/BoxWithArrow';

const Home: React.FC = () => {
    return (
        <div className = {styles.background}>
            <Header />
            <div className = {styles.boxes}>
                <BoxWithArrow
                    imgSrc = {ProductFinder}
                    name = "Product Finder"
                    link = "/ProductFinder"
                />
                <BoxWithArrow
                    imgSrc = {ProductCategorization}
                    name = "Product Categorization"
                    link = "/ProductCategorization"
                />
            </div>
        </div>
    )
}

export default Home