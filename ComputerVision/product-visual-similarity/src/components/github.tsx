import React from 'react';

interface GitHubLinkProps {
    repoUrl: string;
  }

const GitHubLink: React.FC<GitHubLinkProps> = ({ repoUrl }) => {
    return (
      <a href={repoUrl} target="_blank" rel="noopener noreferrer">
        <img 
          src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" 
          alt="GitHub Repo" 
          style={{ width: '50px', height: '50px' }} // Adjust size if needed
        />
      </a>
    );
  };
  
  export default GitHubLink;