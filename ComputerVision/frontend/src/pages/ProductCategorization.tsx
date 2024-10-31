import React, { useState } from "react";
import Header from "../components/Header";
import styles from "./ProductCategorization.module.css";
import axios from "axios";

const ProductCategorization: React.FC = () => {
  const [selectedPhoto, setSelectedPhoto] = useState<string | null>(null);
  const [category, setCategory] = useState<string>("");

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
        "http://localhost:5001/process-image/image-categorization",
        {
          image: image, // Send the Base64 string
        }
      );
      setCategory(response.data);
      console.log(response);
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
              Find Category
            </button>
          </div>
        </div>
        {category && ( // Display the processed category
          <span className={styles.processedCategory}>{category}</span>
        )}
      </div>
    </div>
  );
};

export default ProductCategorization;
