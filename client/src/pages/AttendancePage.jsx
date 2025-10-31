import { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";
import AttendanceTable from "../components/AttendanceTable";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import { useAuth } from "../context/AuthContext";
import {
  Box,
  Typography,
  CircularProgress,
  Alert,
  Fade,
  Paper,
} from "@mui/material";

export default function AttendancePage() {
  const { user } = useAuth();
  const [attendance, setAttendance] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchAttendance = async () => {
      if (!user) return;

      try {
        setLoading(true);
        let endpoint = "/attendance/me"; // ✅ FIXED

        if (user?.role === "manager" || user?.role === "owner") {
          endpoint = "/attendance/all"; // ✅ FIXED
        }

        const res = await axiosClient.get(endpoint);
        setAttendance(res.data || []);
      } catch (err) {
        console.error("❌ Failed to fetch attendance:", err);
        setError("Failed to load attendance data. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchAttendance();
  }, [user]);

  return (
    <Box sx={{ display: "flex", bgcolor: "#f4f6f8", minHeight: "100vh" }}>
      <Sidebar />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          display: "flex",
          flexDirection: "column",
          minHeight: "100vh",
        }}
      >
        <Navbar />

        <Box p={4} flexGrow={1}>
          <Typography variant="h5" fontWeight={600} gutterBottom>
            {user?.role === "manager" || user?.role === "owner"
              ? "Staff Attendance Overview"
              : "My Attendance"}
          </Typography>

          {loading && (
            <Box
              display="flex"
              justifyContent="center"
              alignItems="center"
              height="60vh"
            >
              <CircularProgress size={48} />
            </Box>
          )}

          {!loading && error && (
            <Alert severity="error" sx={{ mt: 3 }}>
              {error}
            </Alert>
          )}

          {!loading && !error && attendance.length === 0 && (
            <Paper
              elevation={3}
              sx={{
                p: 6,
                textAlign: "center",
                borderRadius: 2,
                backgroundColor: "#fff",
              }}
            >
              <Typography variant="h6" color="text.secondary">
                No attendance records found.
              </Typography>
            </Paper>
          )}

          {!loading && !error && attendance.length > 0 && (
            <Fade in timeout={600}>
              <Box>
                <AttendanceTable data={attendance} />
              </Box>
            </Fade>
          )}
        </Box>
      </Box>
    </Box>
  );
}
