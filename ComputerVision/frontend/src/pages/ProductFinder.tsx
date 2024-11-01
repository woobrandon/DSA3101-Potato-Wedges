import React, { useState } from "react";
import styles from "./ProductFinder.module.css";
import axios from "axios";
import Header from "../components/Header";

interface Data {
  image: string;
  about: string;
  product_url: string;
  name: string;
}

const ProductFinder: React.FC = () => {
  const [selectedPhoto, setSelectedPhoto] = useState<string | null>(null);
  const [processedImages, setProcessedImages] = useState<string[] | null>(null);
  const [processedProducts, setProcessedProducts] = useState<string[]>([]);
  const [productUrl, setProductUrl] = useState<string>("");
  const [productAbout, setProductAbout] = useState<string>("");
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
      setProcessedImages(
        response.data.image_search.map((data: Data) => data.image)
      );
      setProcessedProducts(
        response.data.cross_sell.map((data: Data) => data.name)
      );
      setProductUrl(response.data.image_search[0].product_url);
      setProductAbout(response.data.image_search[0].about);
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
              src={`data:image/png;base64,${processedImages[0]}`}
              alt="Processed"
              className={styles.processedImage}
            />
            <div className={styles.description}>
              <a href={productUrl}>Product Link</a>
              <p>
                <strong>Product Name:</strong> {name}
              </p>
              <p>
                <strong>About:</strong> {productAbout}
              </p>
            </div>
          </div>
          <div className={styles.possibleProcessedImageContainer}>
            <p>Other similar products (by image)</p>
            <div className={styles.possibleProcessedImageWrapper}>
              <div>
                {processedImages.slice(1, 5).map((img, id) => (
                  <img
                    key={id}
                    src={`data:image/png;base64,${img}`}
                    alt="Processed"
                    className={styles.processedImagePossible}
                  />
                ))}
              </div>
            </div>
          </div>
          <div className={styles.possibleProcessedImageContainer}>
            <p>Other similar products (by description)</p>
            <div className={styles.possibleProcessedImageWrapper}>
              <div>
                {processedProducts.slice(1, 5).map((name, id) => (
                  <p key={id}>{name}</p>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductFinder;
