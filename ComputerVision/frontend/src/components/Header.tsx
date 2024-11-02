import React, { useState } from "react";
import styles from "./Header.module.css";
import { Navigate, useNavigate } from "react-router-dom";
import logo from "../assets/potato.png"

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
                <div className = {styles.logo}>
                    <img src = {logo} height = "50px" width = "40px"/>
                    <p className = {styles.webTitle}>
                        Potato<br />
                        Wedges<br />
                    </p>
                </div>
                <div className = {styles.appButton}>
                    {headerItems.map((headerItem) => (
                        <div onClick={() => navigateTo(headerItem.path)} className = {styles.headerButton}>
                            {headerItem.label}
                        </div>
                    ))}
                </div>
            </header>
        </div>
    )
}

export default Header