import React, { useState } from "react";
import styles from "./ProductFinder.module.css";
import axios from "axios";
import { Header, ProductCard, ProductCardLong } from "../components";

interface ProcessedImage {
  image: string;
  about: string;
  product_url: string;
  product_price: number;
  name: string;
  product_desc: string;
  category: string;
}

interface ProcessedDescription {
  image: string;
  about: string;
  product_url: string;
  product_price: number;
  name: string;
  product_desc: string;
  category: string;
}

const ProductFinder: React.FC = () => {
  const [selectedPhoto, setSelectedPhoto] = useState<string | null>(null);
  const [processedImages, setProcessedImages] = useState<
    ProcessedImage[] | null
  >(null);
  const [crossSell, setCrossSell] = useState<ProcessedDescription[]>([]);
  const [upSell, setUpSell] = useState<ProcessedDescription[]>([]);
  const [productUrl, setProductUrl] = useState<string>("");
  const [productAbout, setProductAbout] = useState<string>("");
  const [productPrice, setProductPrice] = useState<string>("");
  const [name, setName] = useState<string>("");

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];

    if (file) {
      const reader = new FileReader();

      reader.onloadend = () => {
        // Image stored as a base64 string
        setSelectedPhoto(reader.result as string);
      };

      reader.readAsDataURL(file); // Read the file as a data URL
    }
  };

  const handleProcessImage = async (image: string) => {
    try {
      const response = await axios.post(
        "http://localhost:5001/process-image/image-search",
        {
          image: image, // Send the Base64 string
        }
      );
      console.log(response);
      setProcessedImages(response.data.image_search);
      setCrossSell(response.data.cross_sell);
      setUpSell(response.data.up_sell);
      setProductUrl(response.data.image_search[0].product_url);
      setProductAbout(response.data.image_search[0].about);
      setProductPrice(`₹${response.data.image_search[0].product_price}`);
      setName(response.data.image_search[0].name);
    } catch (error) {
      console.error("Error processing image:", error);
    }
  };

  return (
    <div className={styles.background}>
      <Header />
      <div className={styles.uploadImageContainer}>
        <div className={styles.uploadBox}>
          <h4 className="uploadTitle">Upload Your Image</h4>
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            className={styles.fileInput}
          />
          {selectedPhoto ? (
            <img
              src={selectedPhoto as string}
              alt="Selected"
              className={styles.previewImage}
            />
          ) : (
            <p>No file selected</p>
          )}
          <div className={styles.processImageButtonContainer}>
            <button
              className={styles.processImageButton}
              onClick={() => {
                selectedPhoto && handleProcessImage(selectedPhoto);
              }}
            >
              Find Product
            </button>
          </div>
        </div>
      </div>

      {processedImages && ( // Display the processed image
        <div className={styles.processedImageContainer}>
          <div className={styles.processedImageWrapper}>
            <img
              src={`data:image/png;base64,${processedImages[0].image}`}
              alt="Processed"
              className={styles.processedImage}
            />
            <div className={styles.description}>
              <a href={productUrl} target="_blank">
                Product Link
              </a>
              <p>
                <strong>Product Name:</strong> {name}
              </p>
              <p>
                <strong>About:</strong> {productAbout}
              </p>
              <p>
                <strong>Price:</strong> {productPrice}
              </p>
            </div>
          </div>
          <div className={styles.possibleProcessedImageContainer}>
            <p>Other similar products (by image)</p>
            <div className={styles.possibleProcessedImageWrapper}>
              {processedImages.slice(1, 5).map((data, id) => (
                <ProductCard
                  key={id}
                  imgSrc={`data:image/png;base64,${data.image}`}
                  name={data.name}
                  description={data.product_desc}
                  link={data.product_url}
                />
              ))}
            </div>
          </div>
          <div className={styles.possibleProcessedImageContainer}>
            <p>Other similar products (by description, cross sell)</p>
            <div className={styles.possibleProcessedImageWrapper}>
              {crossSell.slice(1, 5).map((data, id) => (
                <ProductCardLong
                  key={id}
                  imgSrc={`data:image/png;base64,${data.image}`}
                  name={data.name}
                  price={`₹${data.product_price}`}
                  description={data.product_desc}
                  link={data.product_url}
                  about={data.about}
                  category={data.category}
                />
              ))}
            </div>
          </div>
          <div className={styles.possibleProcessedImageContainer}>
            <p>Other similar products (by description, up sell)</p>
            <div className={styles.possibleProcessedImageWrapper}>
              {upSell.slice(1, 5).map((data, id) => (
                <ProductCardLong
                  key={id}
                  imgSrc={`data:image/png;base64,${data.image}`}
                  name={data.name}
                  price={`₹${data.product_price}`}
                  description={data.product_desc}
                  link={data.product_url}
                  about={data.about}
                  category={data.category}
                />
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductFinder;
