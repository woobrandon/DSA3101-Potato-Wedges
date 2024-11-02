import React from 'react';
import styles from './BoxWithArrow.module.css';
import { Navigate, useNavigate } from "react-router-dom";

interface Props {
    name: string;
    link: string;
  }

const BoxWithArrow: React.FC<Props> = ({name, link}) => {
    const navigate = useNavigate();
    const navigateTo = () => {
        navigate(link);
      };

  return (
    <div className = {styles.boxContainer} onClick = {navigateTo}>
        <div className={styles.box}>
        <p>{name}</p>
        </div>
        <div className={styles.arrow}></div>
    </div>
  );
};

export default BoxWithArrow;