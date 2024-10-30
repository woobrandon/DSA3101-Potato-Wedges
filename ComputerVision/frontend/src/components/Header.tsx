import React, { useState } from "react";
import styles from "./Header.module.css";
import { Navigate, useNavigate } from "react-router-dom";

const Header = () => {
    const navigate = useNavigate();
    const headerItems = [
        { label: "Home", path: "/"},
        { label: "ProductFinder", path: "/ProductFinder"},
        { label: "ProductCategorization", path: "/ProductCategorization"},
    ];

    const navigateTo = (path: string) => {
        navigate(path);
      };
    return (
        <div>
            <header className={styles.header}>
                {headerItems.map((headerItem) => (
                    <div onClick={() => navigateTo(headerItem.path)} className = {styles.headerButton}>
                        {headerItem.label}
                    </div>
                ))}
            </header>
        </div>
    )
}

export default Header