import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function MePage() {
  const nav = useNavigate();
  const [me, setMe] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem("access_token");

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      setMe(null);

      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const res = await fetch("http://127.0.0.1:8000/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
          setError(data?.detail ?? "Failed to load /me");
          setLoading(false);
          return;
        }

        setMe(data);
        setLoading(false);
      } catch (err) {
        setError("Network error: " + err.message);
        setLoading(false);
      }
    }

    load();
  }, [token]);

  function logout() {
    localStorage.removeItem("access_token");
    nav("/login");
  }

  return (
    <div style={{ maxWidth: 520 }}>
      <h1>Minuta — Me</h1>

      {!token && (
        <div style={{ marginTop: 12 }}>
          <div style={{ marginBottom: 8, color: "crimson" }}>You are not logged in.</div>
          <Link to="/login">Go to login</Link>
        </div>
      )}

      {token && (
        <div style={{ display: "flex", gap: 12, alignItems: "center", marginTop: 12 }}>
          <button onClick={logout} style={{ padding: 10 }}>
            Logout
          </button>
        </div>
      )}

      {loading && token && <div style={{ marginTop: 16 }}>Loading…</div>}

      {me && (
        <pre style={{ marginTop: 16, background: "#f6f6f6", padding: 12 }}>
          {JSON.stringify(me, null, 2)}
        </pre>
      )}

      {error && <div style={{ marginTop: 16, color: "crimson" }}>{String(error)}</div>}
    </div>
  );
}
