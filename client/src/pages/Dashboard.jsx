// src/pages/Dashboard.jsx
import { Box, CircularProgress, Typography } from "@mui/material";
import { useAuth } from "../context/AuthContext";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import OwnerDashboard from "../components/dashboards/OwnerDashboard";
import ManagerDashboard from "../components/dashboards/ManagerDashboard";
import StaffDashboard from "../components/dashboards/StaffDashboard";

export default function Dashboard() {
  const { user, loading } = useAuth();

  if (loading)
    return (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
        }}
      >
        <CircularProgress />
      </Box>
    );

  if (!user)
    return (
      <Box textAlign="center" mt={10}>
        <Typography variant="h5" color="error">
          You must be logged in to view the dashboard.
        </Typography>
      </Box>
    );

  const role = user.role?.toLowerCase();

  let DashboardContent = null;
  if (role === "owner") DashboardContent = <OwnerDashboard />;
  else if (role === "manager") DashboardContent = <ManagerDashboard />;
  else DashboardContent = <StaffDashboard />;

  return (
    <Box sx={{ display: "flex", bgcolor: "#f5f6fa", minHeight: "100vh" }}>
      {/* <Sidebar /> */}
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
        {DashboardContent}
      </Box>
    </Box>
  );
}
