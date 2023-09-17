import React, { useContext } from "react";
import { SelectedImageContext } from "../Gallery"; // Import the context
import { Box, Button, Divider } from "@mui/material";
import Filter1Icon from "@mui/icons-material/Filter1";
import Filter2Icon from "@mui/icons-material/Filter2";
import Filter3Icon from "@mui/icons-material/Filter3";
import Filter4Icon from "@mui/icons-material/Filter4";
import Filter5Icon from "@mui/icons-material/Filter5";
import Filter6Icon from "@mui/icons-material/Filter6";
import Filter7Icon from "@mui/icons-material/Filter7";
import Filter8Icon from "@mui/icons-material/Filter8";
import Filter9Icon from "@mui/icons-material/Filter9";

const VerticalButtons = () => {
  const buttonStyle = {
    background: "linear-gradient(45deg, #c94b4b 30%, #75254e 90%)",
    borderRadius: "100%", // Make the buttons circular
    width: "50px", // Set the desired button width
    height: "65px", // Set the desired button height
    margin: "10px 10px", // Add margin for spacing between buttons,
    color: "white",
  };
  const buttonContainerStyle = {
    display: "flex",
    flexDirection: "column", // Arrange buttons vertically
    alignItems: "center", // Center buttons horizontally
    mx: 4,
  };

  const iconStyle = {
    fontSize: "32px",
  };

  return (
    <div style={buttonContainerStyle}>
      <Button variant="contained" color="primary" style={buttonStyle}>
        <Filter1Icon style={iconStyle} />
      </Button>
      <Button variant="contained" color="secondary" style={buttonStyle}>
        <Filter2Icon style={iconStyle} />
      </Button>
      <Button variant="contained" color="info" style={buttonStyle}>
        <Filter3Icon style={iconStyle} />
      </Button>
      <Button variant="contained" color="success" style={buttonStyle}>
        <Filter4Icon style={iconStyle} />
      </Button>
      <Button variant="contained" color="warning" style={buttonStyle}>
        <Filter5Icon style={iconStyle} />
      </Button>
      <Button variant="contained" color="error" style={buttonStyle}>
        <Filter6Icon style={iconStyle} />
      </Button>
      <Button variant="contained" color="primary" style={buttonStyle}>
        <Filter7Icon style={iconStyle} />
      </Button>
      <Button variant="contained" color="secondary" style={buttonStyle}>
        <Filter8Icon style={iconStyle} />
      </Button>
    </div>
  );
};

const KeyImage = () => {
  // Use useContext to access the selectedImage state from the context
  const { selectedImage } = useContext(SelectedImageContext);
  return (
    <>
      <Box sx={{ p: 3, py: 4, display: "flex" }}>
        <Box sx={{ maxWidth: "630px" }}>
          {selectedImage ? (
            <div>
              <img
                style={{ maxWidth: "630px", maxHeight: "683px" }}
                src={require(`../../../images/${selectedImage.img}`)} // Display the selected image
                alt={selectedImage.title}
                loading="lazy"
              />
            </div>
          ) : (
            <p>No image selected</p>
          )}
        </Box>
        <Divider orientation="vertical" flexItem />
        <VerticalButtons /> {/* Include the VerticalButtons component */}
      </Box>
    </>
  );
};

export default KeyImage;
