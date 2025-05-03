import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import './UserMenu.css';

const UserMenu: React.FC = () => {
  const { user, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);

  if (!user) return null;

  return (
    <div className="user-menu">
      <button 
        className="user-menu-button"
        onClick={() => setIsOpen(!isOpen)}
      >
        {user.avatar ? (
          <img src={user.avatar} alt={user.username} />
        ) : (
          <div className="user-initial">
            {user.username[0].toUpperCase()}
          </div>
        )}
      </button>

      {isOpen && (
        <div className="user-menu-dropdown">
          <div className="user-info">
            <strong>{user.username}</strong>
            <span>{user.email}</span>
          </div>
          <button onClick={logout} className="logout-button">
            Sign Out
          </button>
        </div>
      )}
    </div>
  );
};

export default UserMenu; 