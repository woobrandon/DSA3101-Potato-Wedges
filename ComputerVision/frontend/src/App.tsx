import React, { useState } from 'react';
import potato from './assets/potato.png';
import styles from './App.module.css';
import GitHubLink from './components/github';
import backgroundImage from "./assets/amazon_background.jpg"

const App: React.FC = () => {
  const [selectedPhoto, setSelectedPhoto] = useState<string | ArrayBuffer | null>(null)

  const backgroundStyle = {
    backgroundImage: `url(${backgroundImage})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    height: '100vh',
    width: '100%',
  };

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];

    if (file) {
      const reader = new FileReader();
    
      reader.onloadend = () => {
        setSelectedPhoto(reader.result);
      };

      reader.readAsDataURL(file); // Read the file as a data URL
    }
  }

  return (
    <div className={styles.background} style={backgroundStyle}>
      <header className={styles.header}>
        <div className={styles.logo}>
          <img src={potato} className={styles.appLogo} alt="logo" />
        </div>
        <div className={styles.gitLogo}>
          <GitHubLink repoUrl="https://github.com/woobrandon/E-commerce-Performance-Analysis-and-Optimization" />
        </div>
      </header>
      <div className={styles.uploadImageContainer}>
        <h2 className="uploadTitle">Upload Your Image</h2>
        <div className = {styles.uploadBox}>
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
    </div>
  );
}

export default App;
