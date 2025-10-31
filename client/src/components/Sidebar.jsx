import {
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
  Box,
} from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import PeopleIcon from "@mui/icons-material/People";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import LogoutIcon from "@mui/icons-material/Logout";
import { useLocation, useNavigate } from "react-router-dom";

export default function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    { text: "Dashboard", icon: <DashboardIcon />, path: "/dashboard" },
    { text: "Users", icon: <PeopleIcon />, path: "/users" },
    { text: "Attendance", icon: <AccessTimeIcon />, path: "/attendance" },
  ];

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <Drawer
      variant="permanent"
      anchor="left"
      sx={{
        width: 240,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: 240,
          background: "linear-gradient(180deg, #1e1e2f 0%, #2d2d44 100%)",
          color: "#fff",
          borderRight: "none", // ✅ removes visible line
          boxShadow: "none",   // ✅ removes shadow gap
          top: 0,              // ✅ ensures it’s fully flush
          left: 0,
          bottom: 0,
        },
      }}
    >
      {/* App Title */}
      <Box
        sx={{
          p: 3,
          textAlign: "center",
          borderBottom: "1px solid rgba(255,255,255,0.1)",
        }}
      >
        <Typography
          variant="h6"
          fontWeight="bold"
          sx={{
            background: "linear-gradient(to right, #00bcd4, #2196f3)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
          }}
        >
          Retail Admin
        </Typography>
      </Box>

      {/* Navigation Menu */}
      <List sx={{ mt: 1 }}>
        {menuItems.map((item) => {
          const active = location.pathname === item.path;
          return (
            <ListItemButton
              key={item.text}
              onClick={() => navigate(item.path)}
              sx={{
                mx: 1,
                mb: 0.5,
                borderRadius: 1,
                backgroundColor: active
                  ? "rgba(255, 255, 255, 0.1)"
                  : "transparent",
                "&:hover": {
                  backgroundColor: "rgba(255, 255, 255, 0.15)",
                },
                transition: "background 0.2s ease-in-out",
              }}
            >
              <ListItemIcon sx={{ color: "#fff", minWidth: 40 }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText
                primary={item.text}
                primaryTypographyProps={{
                  fontWeight: active ? "bold" : "normal",
                  color: active ? "#00bcd4" : "#fff",
                }}
              />
            </ListItemButton>
          );
        })}
      </List>

      {/* Logout Button */}
      <Box
        sx={{
          position: "absolute",
          bottom: 20,
          width: "100%",
        }}
      >
        <ListItemButton
          onClick={handleLogout}
          sx={{
            mx: 1,
            borderRadius: 1,
            "&:hover": {
              backgroundColor: "rgba(255, 255, 255, 0.1)",
            },
          }}
        >
          <ListItemIcon sx={{ color: "#ff5252", minWidth: 40 }}>
            <LogoutIcon />
          </ListItemIcon>
          <ListItemText
            primary="Logout"
            primaryTypographyProps={{
              color: "#ff5252",
              fontWeight: "bold",
            }}
          />
        </ListItemButton>
      </Box>
    </Drawer>
  );
}
