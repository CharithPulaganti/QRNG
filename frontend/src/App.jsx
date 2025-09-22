import { useState } from "react";
import Dashboard from "./components/Dashboard";
import TokenGenerator from "./components/TokenGenerator";
import RandomnessReport from "./components/RandomnessReport";

export default function App() {
  const [darkMode, setDarkMode] = useState(false);

  const appStyle = {
    backgroundColor: darkMode ? "#1e1e1e" : "#f9f9f9",
    color: darkMode ? "#f9f9f9" : "#222",
    minHeight: "100vh",
    padding: "20px",
    transition: "all 0.3s ease",
    fontFamily: "system-ui, sans-serif",
  };

  const sectionStyle = {
    background: darkMode ? "#2a2a2a" : "white",
    padding: "20px",
    borderRadius: "12px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
    transition: "all 0.3s ease",
    maxWidth: "800px",
    margin: "20px auto",
  };

  const buttonStyle = {
    padding: "10px 16px",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    color: "white",
    background: "#007bff",
    marginTop: "10px",
    transition: "background 0.3s ease",
  };

  const copyBtnStyle = {
    ...buttonStyle,
    background: "#28a745",
  };

  return (
    <div style={appStyle}>
      {/* Dark mode toggle */}
      <button
        onClick={() => setDarkMode(!darkMode)}
        style={{
          position: "absolute",
          top: 20,
          right: 20,
          padding: "8px 14px",
          borderRadius: "8px",
          border: "none",
          background: darkMode ? "#444" : "#222",
          color: "white",
          cursor: "pointer",
        }}
      >
        {darkMode ? "☀ Light Mode" : "🌙 Dark Mode"}
      </button>

      {/* Title */}
      <h1 style={{ textAlign: "center" }}>
        QRNG — Quantum Random Number Generator
      </h1>
      <p style={{ textAlign: "center", opacity: 0.8 }}>
        Live quantum bits (Qiskit if available) with extractor pipeline and statistical tests.
      </p>

      {/* Dashboard */}
      <div style={sectionStyle}>
        <Dashboard />
      </div>

      {/* Randomness Report */}
      <div style={sectionStyle}>
        <h2>Randomness Report</h2>
        <RandomnessReport />
      </div>

      <hr style={{ margin: "24px 0" }} />

      {/* Token Generator */}
      <div style={sectionStyle}>
        <h2>Custom Key Generator</h2>
        <TokenGenerator buttonStyle={buttonStyle} copyBtnStyle={copyBtnStyle} />
      </div>
    </div>
  );
}
