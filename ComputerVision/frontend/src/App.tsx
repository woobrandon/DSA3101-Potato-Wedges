import React, { useState } from "react";
import potato from "./assets/potato.png";
import styles from "./App.module.css";
import GitHubLink from "./components/github";
import backgroundImage from "./assets/amazon_background.jpg";
import axios from "axios";

const App: React.FC = () => {
  const [selectedPhoto, setSelectedPhoto] = useState<string | null>(null);
  const [processedImage, setProcessedImage] = useState<string | null>(null);
  const [productUrl, setProductUrl] = useState<string | null> (null);

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
      console.log(processedImage);
      setProcessedImage(processedImage);
      console.log(response);
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
        <h2 className="uploadTitle">Upload Your Image</h2>
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
        </div>
      </div>
      <div className = {styles.processImageButtonContainer}>
        <button className={styles.processImageButton} onClick ={() => {selectedPhoto && handleProcessImage(selectedPhoto)}}>
          Find Product
        </button>
      </div>
      {processedImage && ( // Display the processed image
        <div className={styles.processedImageContainer}>
          <img
            src={`data:image/png;base64,${processedImage}`}
            alt="Processed"
            className={styles.processedImage}
          />
          <a>Click here to go to website</a>
        </div>
      )}
    </div>
  );
};

export default App;
