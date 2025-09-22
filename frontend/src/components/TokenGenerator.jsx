import { useState } from "react";

export default function TokenGenerator({ darkMode = false }) {
  const [kind, setKind] = useState("numeric");
  const [length, setLength] = useState(16);
  const [tokens, setTokens] = useState([]);

  // Function to call backend API
  async function handleGenerate() {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/token", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ kind, length }),
      });

      const data = await res.json();

      if (data.token) {
        setTokens((prev) => [data.token, ...prev]);
      } else {
        setTokens((prev) => [
          "❌ Error: " + (data.error || "Unknown"),
          ...prev,
        ]);
      }
    } catch (err) {
      console.error(err);
      setTokens((prev) => ["❌ Failed to connect to backend", ...prev]);
    }
  }

  // 🎨 Theme styles
  const theme = {
    container: {
      padding: "20px",
      maxWidth: "500px",
      margin: "0 auto",
      borderRadius: "12px",
      boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
      background: darkMode ? "#1e1e2f" : "#fff",
      color: darkMode ? "#f9fafb" : "#111827",
    },
    input: {
      width: "100%",
      padding: "8px",
      borderRadius: "6px",
      border: "1px solid",
      borderColor: darkMode ? "#374151" : "#ccc",
      marginBottom: "12px",
      background: darkMode ? "#111827" : "#fff",
      color: darkMode ? "#f9fafb" : "#111827",
    },
    select: {
      width: "100%",
      padding: "8px",
      borderRadius: "6px",
      border: "1px solid",
      borderColor: darkMode ? "#374151" : "#ccc",
      marginBottom: "12px",
      background: darkMode ? "#111827" : "#fff",
      color: darkMode ? "#f9fafb" : "#111827",
    },
    generateBtn: {
      width: "100%",
      padding: "10px 16px",
      borderRadius: "8px",
      border: "none",
      cursor: "pointer",
      color: "white",
      background: "#3b82f6",
      marginBottom: "12px",
    },
    tokenBox: {
      marginTop: "14px",
      padding: "10px",
      borderRadius: "6px",
      wordBreak: "break-all",
      background: darkMode ? "#2d2d3a" : "#f1f1f1",
      color: darkMode ? "#f9fafb" : "#111827",
    },
    copyBtn: {
      padding: "8px 12px",
      borderRadius: "6px",
      border: "none",
      cursor: "pointer",
      color: "white",
      background: "#10b981",
      marginTop: "6px",
    },
  };

  return (
    <div style={theme.container}>
      <h2 style={{ fontSize: "20px", fontWeight: "bold", marginBottom: "10px" }}>
        🔑 Random Token Generator
      </h2>

      <label style={{ display: "block", marginBottom: "6px" }}>Length</label>
      <input
        type="number"
        min="4"
        max="64"
        value={length}
        onChange={(e) => setLength(Number(e.target.value))}
        style={theme.input}
      />

      <label style={{ display: "block", marginBottom: "6px" }}>Kind</label>
      <select
        value={kind}
        onChange={(e) => setKind(e.target.value)}
        style={theme.select}
      >
        <option value="numeric">Numeric</option>
        <option value="alpha">Alphabet</option>
        <option value="special">Special Characters</option>
        <option value="alphanumeric">Alphanumeric</option>
        <option value="alpha_special">Alphabet + Special</option>
        <option value="all">All Characters</option>
      </select>

      <button onClick={handleGenerate} style={theme.generateBtn}>
        🎲 Generate Token
      </button>

      {tokens.map((t, idx) => (
        <div key={idx} style={theme.tokenBox}>
          <p style={{ fontFamily: "monospace" }}>{t}</p>
          <button
            style={theme.copyBtn}
            onClick={() => navigator.clipboard.writeText(t)}
          >
            📋 Copy
          </button>
        </div>
      ))}
    </div>
  );
}
