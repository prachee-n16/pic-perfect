import React from "react";

import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";

import "./Navbar.css";

const Navbar = () => {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar
        position="static"
        sx={{
          fontFamily: "Poppins, sans-serif",
          backgroundColor: "#000000",
        }}
      >
        <Toolbar sx={{ backgroundColor: "#000000" }}>
          <Typography variant="h1" style={{ fontSize: "24px", px: 5 }}>
            pic
          </Typography>
          <Typography
            style={{
              fontWeight: "bold",
              fontSize: "16px",
              marginBottom: "-5px",
              marginLeft: "1px",
            }}
            variant="h1"
          >
            •
          </Typography>
          <Typography
            style={{
              background: "linear-gradient(45deg, #c94b4b 30%, #75254e 90%)",
              WebkitBackgroundClip: "text", // Note: Use 'Webkit' with an uppercase 'W'
              WebkitTextFillColor: "transparent", // Note: Use 'Webkit' with an uppercase 'W'
              marginLeft: "1px",
              fontWeight: "bold",
              fontSize: "24px",
            }}
            variant="h1"
          >
            perfect!
          </Typography>
        </Toolbar>
        <Divider sx={{ border: "0.1px solid #1F1F1F" }} />
      </AppBar>
    </Box>
  );
};

export default Navbar;
