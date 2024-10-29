import React, { useState } from "react";
import potato from "./assets/potato.png";
import styles from "./App.module.css";
import GitHubLink from "./components/github";
import backgroundImage from "./assets/amazon_background.jpg";
import axios from "axios";

const App: React.FC = () => {
  const [selectedPhoto, setSelectedPhoto] = useState<string | null>(null);
  const [processedImage, setProcessedImage] = useState<string | null>(null);
  const [productUrl, setProductUrl] = useState<string> ("");
  const [productAbout, setProductAbout] = useState<string>("");

  const backgroundStyle = {
    backgroundImage: `url(${backgroundImage})`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    backgroundRepeat: "no-repeat",
    height: "100vh",
    width: "100%",
  };

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

      const processedImage  = response.data.image;
      setProcessedImage(processedImage);
      setProductUrl(response.data.product_url);
      setProductAbout(response.data.about);
      console.log(response.data.about)
    } catch (error) {
      console.error("Error processing image:", error);
    }
  };

  return (
    <div className={styles.background} style={backgroundStyle}>
      <header className={styles.header}>
        <p className = {styles.webTitle}>Amazon Product Finder</p>
      </header>
      <div className={styles.uploadImageContainer}>
        <h3 className="uploadTitle">Upload Your Image</h3>
        <div className={styles.uploadBox}>
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
              className={styles.previewImage} // Move styles to CSS module
            />
          ) : (
            <p>No file selected</p>
          )}
          <div className = {styles.processImageButtonContainer}>
            <button className={styles.processImageButton} onClick ={() => {selectedPhoto && handleProcessImage(selectedPhoto)}}>
              Find Product
            </button>
          </div>
        </div>
      </div>
      {processedImage && ( // Display the processed image
        <div className={styles.processedImageContainer}>
          <div className={styles.processedImageWrapper}>
            <img
              src={`data:image/png;base64,${processedImage}`}
              alt="Processed"
              className={styles.processedImage}
            />
            <div className = {styles.description}>
              <a href = {productUrl}>Product URL</a>
              <p>{productAbout}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
