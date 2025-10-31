import * as React from "react";
import { DataGrid } from "@mui/x-data-grid";
import { Box, Typography, Paper } from "@mui/material";

export default function AttendanceTable({ data = [] }) {
  // ✅ Detect if data includes staff fields (manager/owner view)
  const isManagerView = data.some((r) => r.staff_name || r.staff_email);

  // ✅ Define columns dynamically
  const columns = [
    ...(isManagerView
      ? [
          {
            field: "staff_name",
            headerName: "Staff Name",
            flex: 1,
            headerAlign: "center",
            align: "center",
          },
          {
            field: "staff_email",
            headerName: "Staff Email",
            flex: 1.3,
            headerAlign: "center",
            align: "center",
          },
        ]
      : []),
    {
      field: "date",
      headerName: "Date",
      flex: 1,
      headerAlign: "center",
      align: "center",
    },
    {
      field: "first_login",
      headerName: "First Login",
      flex: 1,
      headerAlign: "center",
      align: "center",
    },
    {
      field: "last_logout",
      headerName: "Last Logout",
      flex: 1,
      headerAlign: "center",
      align: "center",
    },
    {
      field: "total_seconds",
      headerName: "Total Time (hrs)",
      flex: 1,
      headerAlign: "center",
      align: "center",
      valueGetter: (params) => {
        const secs = params?.row?.total_seconds;
        if (!secs || isNaN(secs)) return "0.00";
        return (secs / 3600).toFixed(2);
      },
    },
  ];

  // ✅ Ensure each row has a unique id
  const rows = data.map((r, i) => ({ id: r.id || i + 1, ...r }));

  return (
    <Paper
      elevation={4}
      sx={{
        p: 3,
        mt: 3,
        borderRadius: 2,
        backgroundColor: "#fff",
      }}
    >
      <Typography variant="h6" fontWeight={600} mb={2}>
        Attendance Records
      </Typography>

      <Box sx={{ height: 520, width: "100%" }}>
        <DataGrid
          rows={rows}
          columns={columns}
          pageSize={7}
          rowsPerPageOptions={[7, 14, 21]}
          disableRowSelectionOnClick
          sx={{
            border: "none",
            "& .MuiDataGrid-columnHeaders": {
              backgroundColor: "#000", // 🖤 Black header
              color: "black", // White text
              fontWeight: "bold",
              fontSize: "1rem",
              minHeight: "56px !important",
              alignItems: "center",
            },
            "& .MuiDataGrid-columnHeaderTitle": {
              whiteSpace: "normal",
              lineHeight: "1.5rem",
              textAlign: "center",
              width: "100%",
            },
            "& .MuiDataGrid-row:hover": {
              backgroundColor: "#f5f5f5",
            },
            "& .MuiDataGrid-cell": {
              textAlign: "center",
              fontSize: "0.95rem",
              padding: "10px 0",
            },
          }}
        />
      </Box>
    </Paper>
  );
}
