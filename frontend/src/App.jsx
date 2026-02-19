import { BrowserRouter, Routes, Route, Navigate, Link } from "react-router-dom";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import MePage from "./pages/MePage";

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ maxWidth: 520, margin: "40px auto", fontFamily: "sans-serif" }}>
        <header style={{ display: "flex", gap: 12, marginBottom: 20 }}>
          <Link to="/register">Register</Link>
          <Link to="/login">Login</Link>
          <Link to="/me">Me</Link>
        </header>

        <Routes>
          {/* стартовая страница */}
          <Route path="/" element={<Navigate to="/register" replace />} />

          {/* страницы SPA */}
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/me" element={<MePage />} />

          {/* fallback */}
          <Route path="*" element={<div>404</div>} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
