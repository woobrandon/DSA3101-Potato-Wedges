import React from 'react';
import styles from './Home.module.css';
import Header from '../components/Header';

const Home: React.FC = () => {
    return (
        <div className = {styles.background}>
            <Header />
            <div className = {styles.bodyTextContainer}>
                <div className = {styles.bodyTextWrapper}>
                    <div className = {styles.bodyText}>
                    Hi!<br /><br />
    
                    Welcome to Amazon Product Helper. This is a free-to-use website and please leave a review in Contact Us to let us know of any issues or new features you wish to add. Enjoy your stay here!<br /><br />

                    Thanks,<br />
                    Potato Wedges Group
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Home