import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Avatar,
  Tooltip,
} from "@mui/material";
import LogoutIcon from "@mui/icons-material/Logout";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { logout } = useAuth();

  return (
    <AppBar
      position="sticky"
      elevation={3}
      sx={{
        background: "linear-gradient(90deg, #1976d2 0%, #42a5f5 100%)",
        color: "#fff",
        zIndex: (theme) => theme.zIndex.drawer + 1, // Stay above sidebar
      }}
    >
      <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
        {/* Left side: Logo / Title */}
        <Typography
          variant="h6"
          sx={{
            fontWeight: "bold",
            letterSpacing: 0.5,
            display: "flex",
            alignItems: "center",
            gap: 1,
          }}
        >
          🛍️ Retail Shop Management
        </Typography>

        {/* Right side: Profile + Logout */}
        <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
          {/* Placeholder avatar for user */}
          <Tooltip title="User Profile (Coming soon)">
            <Avatar
              sx={{
                bgcolor: "#fff",
                color: "#1976d2",
                width: 32,
                height: 32,
                fontSize: "0.9rem",
                fontWeight: "bold",
              }}
            >
              R
            </Avatar>
          </Tooltip>

          <Button
            variant="outlined"
            startIcon={<LogoutIcon />}
            onClick={logout}
            sx={{
              color: "#fff",
              borderColor: "rgba(255,255,255,0.5)",
              "&:hover": {
                borderColor: "#fff",
                backgroundColor: "rgba(255,255,255,0.1)",
              },
              textTransform: "none",
              fontWeight: 500,
            }}
          >
            Logout
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}
