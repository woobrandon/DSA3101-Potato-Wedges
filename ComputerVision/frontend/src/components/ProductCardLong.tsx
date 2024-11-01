import React from "react";
import styles from "./ProductCardLong.module.css";

interface Props {
  imgSrc: string;
  name: string;
  description: string;
  link: string;
  about: string;
  category: string;
}

const ProductCardLong: React.FC<Props> = ({
  imgSrc,
  name,
  description,
  link,
  about,
  category,
}) => {
  return (
    <section className={styles.ProductCardBorder}>
      <a href={link} target="_blank" rel="noopener noreferrer">
        <div className={styles.ProductCardMainImg}>
          <img src={imgSrc} alt="" className={styles.ProductCardImage} />
          <h3>{name}</h3>
          <p>{description}</p>
        </div>
      </a>
      <div className={styles.ProductCardMainDescription}>
        <p>
          <span>
            <strong>About: </strong> {about}
          </span>
          <br />
          <strong>Category: </strong> {category}
        </p>
      </div>
    </section>
  );
};

export default ProductCardLong;
