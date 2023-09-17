import React, { useState, useContext, useEffect } from "react"; // Import useContext
import { Box } from "@mui/material";
import ImageList from "@mui/material/ImageList";
import ImageListItem from "@mui/material/ImageListItem";
import { SelectedImageContext } from "../Gallery"; // Import the context
import raw from "./../../../imagesInfo.txt";

const ImageGrid = () => {
  const { selectedImage, setSelectedImage } = useContext(SelectedImageContext);
  const [fileContent, setFileContent] = useState("");
  const [entries, setEntries] = useState("");
  var textBlock = "";
  const handleImageClick = (item) => {
    // When an image is clicked, update the state with image path and title
    setSelectedImage(item);
  };

  const itemData = [
    {
      img: "capture_20230917_060145.jpeg",
    },
    {
      img: "capture_20230917_060221.jpeg",
    },
    {
      img: "capture_20230917_060222.jpeg",
    },
  ];

  return (
    <Box sx={{ p: 3, py: 2 }}>
      <ImageList
        sx={{ width: "50vw", height: "30vh" }}
        cols={3}
        gap={16} // Adjust the gap size as needed
      >
        {itemData.map((item) => (
          <ImageListItem
            key={item.img}
            sx={{
              margin: "8px",
              border: "1px solid transparent",
              backgroundImage:
                "linear-gradient(45deg, #c94b4b 30%, #75254e 90%)",
              cursor: "pointer", // Add a pointer cursor to indicate interactivity
              transition:
                "border-width 0.3s ease-in-out, opacity 0.3s ease-in-out", // Add transition
              "&:hover": {
                border: "2px solid transparent", // Increase border width on hover
                opacity: 0.7, // Decrease opacity on hover
              },
            }}
            onClick={() => handleImageClick(item)} // Call handleImageClick with the clicked item
          >
            <img
              src={require(`../../../captures/${item.img}`)} // Replace with your local image path
              loading="lazy"
            />
          </ImageListItem>
        ))}
      </ImageList>
    </Box>
  );
};

export default ImageGrid;
