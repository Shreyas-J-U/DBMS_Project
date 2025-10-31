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
import PaymentIcon from "@mui/icons-material/Payment";

export default function OwnerDashboard() {
  return (
    <Box p={4} flexGrow={1}>
      <Typography variant="h4" fontWeight={600} gutterBottom>
        Owner Dashboard 🧑‍💼
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" mb={3}>
        Manage your entire retail system from one place.
      </Typography>

      <Divider sx={{ mb: 4 }} />

      <Grid container spacing={3}>
        <DashboardCard
          icon={<PeopleAltIcon color="primary" sx={{ fontSize: 40 }} />}
          title="User Management"
          desc="Add or manage managers, staff, and suppliers."
          btn="Manage Users"
        />
        <DashboardCard
          icon={<AccessTimeIcon color="primary" sx={{ fontSize: 40 }} />}
          title="Attendance"
          desc="View attendance of all staff members."
          btn="View Attendance"
        />
        <DashboardCard
          icon={<PaymentIcon color="primary" sx={{ fontSize: 40 }} />}
          title="Payments"
          desc="Manage transactions and staff salaries."
          btn="Go to Payments"
        />
        <DashboardCard
          icon={<InventoryIcon color="primary" sx={{ fontSize: 40 }} />}
          title="Stock Management"
          desc="View and update inventory levels."
          btn="View Stock"
        />
        <DashboardCard
          icon={<InsightsIcon color="primary" sx={{ fontSize: 40 }} />}
          title="Reports & Insights"
          desc="Analyze overall shop performance and revenue."
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
