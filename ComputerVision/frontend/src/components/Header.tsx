import React, { useState } from "react";
import styles from "./Header.module.css"

const Header = () => {
    return (
        <div>
            <header className={styles.header}>
                <p className = {styles.webTitle}>Amazon Product Finder</p>
            </header>
        </div>
    )
}

export default Header