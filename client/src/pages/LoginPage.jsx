import { useState } from "react";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { Box, Button, TextField, Typography, Alert, CircularProgress } from "@mui/material";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const response = await axios.post(
        "http://127.0.0.1:8000/api/token",
        formData,
        {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        }
      );

      console.log("✅ Login successful:", response.data);

      const token = response.data?.access_token;
      if (!token) throw new Error("No token received");

      // ✅ Decode token to extract role + user_id
      const decoded = jwtDecode(token);
      console.log("Decoded JWT:", decoded);

      // Example payload: { user_id: 5, role: "manager", exp: 1730458394 }

      const userData = {
        id: decoded.user_id,
        role: decoded.role,
      };

      // Save to localStorage
      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(userData));

      // Update context
      login(token, userData);

      navigate("/dashboard");
    } catch (err) {
      console.error("❌ Login error:", err);
      if (err.response?.status === 400) {
        setError("Incorrect email or password");
      } else if (err.response?.status === 422) {
        setError("Invalid input fields");
      } else {
        setError("Server connection failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      display="flex"
      alignItems="center"
      justifyContent="center"
      minHeight="100vh"
      sx={{ backgroundColor: "#f5f6fa" }}
    >
      <Box
        component="form"
        onSubmit={handleLogin}
        sx={{
          p: 4,
          borderRadius: 2,
          boxShadow: 3,
          backgroundColor: "white",
          width: "100%",
          maxWidth: 400,
        }}
      >
        <Typography variant="h5" textAlign="center" mb={2}>
          Retail Shop Login
        </Typography>

        <TextField
          label="Email"
          type="email"
          fullWidth
          margin="normal"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <TextField
          label="Password"
          type="password"
          fullWidth
          margin="normal"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}

        <Button
          type="submit"
          variant="contained"
          fullWidth
          sx={{ mt: 3 }}
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : "Login"}
        </Button>
      </Box>
    </Box>
  );
}
