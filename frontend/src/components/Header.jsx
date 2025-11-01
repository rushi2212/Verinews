import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./Header.css";

const Header = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <header className="app-header">
      <div className="header-content">
        <div
          className="logo"
          onClick={() => navigate("/")}
          style={{ cursor: "pointer" }}
        >
          <h1>� VeriNews</h1>
          <span>AI-Powered News Verification</span>
        </div>

        <nav className="nav-links">
          <a
            onClick={() => navigate("/")}
            className={`nav-link ${isActive("/") ? "active" : ""}`}
          >
            Home
          </a>
          <a
            onClick={() => navigate("/how-it-works")}
            className={`nav-link ${isActive("/how-it-works") ? "active" : ""}`}
          >
            How It Works
          </a>
        </nav>
      </div>
    </header>
  );
};

export default Header;
