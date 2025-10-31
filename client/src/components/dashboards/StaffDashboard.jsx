import {
  Box,
  Typography,
  Grid,
  Paper,
  Divider,
  Button,
} from "@mui/material";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import InventoryIcon from "@mui/icons-material/Inventory";

export default function StaffDashboard() {
  return (
    <Box p={4} flexGrow={1}>
      <Typography variant="h4" fontWeight={600} gutterBottom>
        Staff Dashboard 👷
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" mb={3}>
        Access your attendance and manage assigned inventory.
      </Typography>

      <Divider sx={{ mb: 4 }} />

      <Grid container spacing={3}>
        <DashboardCard
          icon={<AccessTimeIcon color="primary" sx={{ fontSize: 40 }} />}
          title="My Attendance"
          desc="View your recent login and logout history."
          btn="View Attendance"
        />
        <DashboardCard
          icon={<InventoryIcon color="primary" sx={{ fontSize: 40 }} />}
          title="Inventory"
          desc="View items assigned to you or update stock status."
          btn="View Inventory"
        />
      </Grid>
    </Box>
  );
}

function DashboardCard({ icon, title, desc, btn }) {
  return (
    <Grid item xs={12} md={6}>
      <Paper
        elevation={3}
        sx={{
          p: 3,
          borderRadius: 2,
          display: "flex",
          flexDirection: "column",
          gap: 2,
          alignItems: "flex-start",
          transition: "all 0.3s ease",
          "&:hover": { transform: "translateY(-4px)", boxShadow: 6 },
        }}
      >
        {icon}
        <Box>
          <Typography variant="h6">{title}</Typography>
          <Typography variant="body2" color="text.secondary" mb={2}>
            {desc}
          </Typography>
          <Button variant="contained" size="small">
            {btn}
          </Button>
        </Box>
      </Paper>
    </Grid>
  );
}
