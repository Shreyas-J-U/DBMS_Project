import { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import {
  Box,
  Typography,
  CircularProgress,
  Alert,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Fade,
} from "@mui/material";

export default function UsersPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await axiosClient.get("/users_list");
        setUsers(res.data || []);
      } catch (err) {
        console.error("Failed to fetch users:", err);
        setError("Unable to load users. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  return (
    <Box sx={{ display: "flex", backgroundColor: "#f4f6f8", minHeight: "100vh" }}>
      <Sidebar />

      <Box sx={{ flexGrow: 1, ml: 25 }}>
        <Navbar />
        <Box p={3}>
          <Typography variant="h5" fontWeight={600} gutterBottom>
            User Management
          </Typography>
          <Typography variant="body2" color="text.secondary" mb={2}>
            View all registered users, their roles, and contact details.
          </Typography>

          {/* Loading */}
          {loading && (
            <Box display="flex" justifyContent="center" alignItems="center" height="60vh">
              <CircularProgress />
            </Box>
          )}

          {/* Error */}
          {!loading && error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}

          {/* Empty */}
          {!loading && !error && users.length === 0 && (
            <Paper
              elevation={3}
              sx={{
                p: 5,
                textAlign: "center",
                borderRadius: 2,
                backgroundColor: "#fff",
              }}
            >
              <Typography variant="h6" color="text.secondary">
                No users found.
              </Typography>
            </Paper>
          )}

          {/* Users Table */}
          {!loading && !error && users.length > 0 && (
            <Fade in timeout={500}>
              <TableContainer component={Paper} elevation={3} sx={{ borderRadius: 2 }}>
                <Table>
                  <TableHead>
                    <TableRow sx={{ backgroundColor: "#1976d2" }}>
                      <TableCell sx={{ color: "white", fontWeight: 600 }}>ID</TableCell>
                      <TableCell sx={{ color: "white", fontWeight: 600 }}>Name</TableCell>
                      <TableCell sx={{ color: "white", fontWeight: 600 }}>Email</TableCell>
                      <TableCell sx={{ color: "white", fontWeight: 600 }}>Role</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {users.map((user, index) => (
                      <TableRow
                        key={user.id}
                        sx={{
                          backgroundColor: index % 2 === 0 ? "#fafafa" : "#fff",
                          "&:hover": { backgroundColor: "#e3f2fd" },
                          transition: "background-color 0.2s ease",
                        }}
                      >
                        <TableCell>{user.id}</TableCell>
                        <TableCell>{user.name}</TableCell>
                        <TableCell>{user.email}</TableCell>
                        <TableCell
                          sx={{
                            textTransform: "capitalize",
                            color:
                              user.role === "manager"
                                ? "primary.main"
                                : user.role === "owner"
                                ? "success.main"
                                : "text.primary",
                            fontWeight: 500,
                          }}
                        >
                          {user.role}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Fade>
          )}
        </Box>
      </Box>
    </Box>
  );
}
