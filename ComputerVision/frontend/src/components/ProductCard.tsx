import React from "react";
import styles from "./ProductCard.module.css";

interface Props {
  imgSrc: string;
  name: string;
  description: string;
  link: string;
}

const ProductCard: React.FC<Props> = ({ imgSrc, name, description, link }) => {
  return (
    <section className={styles.ProductCardBorder}>
      <a href={link} target="_blank" rel="noopener noreferrer">
        <div className={styles.ProductCardMain}>
          <img src={imgSrc} alt="" className={styles.ProductCardImage} />
          <h3>{name}</h3>
          <p>{description}</p>
        </div>
      </a>
    </section>
  );
};

export default ProductCard;
