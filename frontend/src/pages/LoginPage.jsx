import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function onSubmit(e) {
    e.preventDefault();
    setResult(null);
    setError(null);

    try {
      const form = new URLSearchParams();
      // FastAPI OAuth2PasswordRequestForm ждёт username, не email
      form.set("username", email);
      form.set("password", password);

      const res = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: form.toString(),
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        setError(data?.detail ?? "Login failed");
        return;
      }

      // строго по твоей схеме ответа
      localStorage.setItem("access_token", data.access_token);

      setResult(data);
      nav("/me");
    } catch (err) {
      setError("Network error: " + err.message);
    }
  }

  return (
    <div style={{ maxWidth: 420 }}>
      <h1>Minuta — Login</h1>

      <form onSubmit={onSubmit} style={{ display: "grid", gap: 12 }}>
        <label>
          Email
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            type="email"
            required
            style={{ width: "100%", padding: 8 }}
          />
        </label>

        <label>
          Password
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            required
            style={{ width: "100%", padding: 8 }}
          />
        </label>

        <button type="submit" style={{ padding: 10 }}>
          Login
        </button>
      </form>

      {result && (
        <pre style={{ marginTop: 16, background: "#f6f6f6", padding: 12 }}>
          {JSON.stringify(result, null, 2)}
        </pre>
      )}

      {error && <div style={{ marginTop: 16, color: "crimson" }}>{String(error)}</div>}
    </div>
  );
}
