    import {
  Box,
  Typography,
  Grid,
  Paper,
  Divider,
  Button,
} from "@mui/material";
import PeopleAltIcon from "@mui/icons-material/PeopleAlt";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import InsightsIcon from "@mui/icons-material/Insights";
import InventoryIcon from "@mui/icons-material/Inventory";

export default function ManagerDashboard() {
  return (
    <Box p={4} flexGrow={1}>
      <Typography variant="h4" fontWeight={600} gutterBottom>
        Manager Dashboard 👔
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" mb={3}>
        Oversee staff, attendance, and stocks efficiently.
      </Typography>

      <Divider sx={{ mb: 4 }} />

      <Grid container spacing={3}>
        <DashboardCard
          icon={<PeopleAltIcon color="primary" sx={{ fontSize: 40 }} />}
          title="Staff Management"
          desc="Add or manage staff accounts."
          btn="Manage Staff"
        />
        <DashboardCard
          icon={<AccessTimeIcon color="primary" sx={{ fontSize: 40 }} />}
          title="Attendance"
          desc="View and track staff attendance records."
          btn="View Attendance"
        />
        <DashboardCard
          icon={<InventoryIcon color="primary" sx={{ fontSize: 40 }} />}
          title="Inventory"
          desc="Track stock levels and manage items."
          btn="View Inventory"
        />
        <DashboardCard
          icon={<InsightsIcon color="primary" sx={{ fontSize: 40 }} />}
          title="Reports"
          desc="Monitor shop performance and daily metrics."
          btn="View Reports"
        />
      </Grid>
    </Box>
  );
}

function DashboardCard({ icon, title, desc, btn }) {
  return (
    <Grid item xs={12} md={4}>
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
