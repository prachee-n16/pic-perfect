import React, { useContext } from "react"; // Import useContext
import { Box } from "@mui/material";
import ImageList from "@mui/material/ImageList";
import ImageListItem from "@mui/material/ImageListItem";
import { SelectedImageContext } from "../Gallery"; // Import the context

const ImageGrid = () => {
  const { selectedImage, setSelectedImage } = useContext(SelectedImageContext);

  const handleImageClick = (item) => {
    // When an image is clicked, update the state with image path and title
    setSelectedImage(item);
  };

  // Define or import your itemData array here
  const itemData = [
    {
      img: "1.jpeg",
      title: "Image 1",
    },
    {
      img: "2.jpeg",
      title: "Image 2",
    },
    {
      img: "3.jpeg",
      title: "Image 3",
    },
    {
      img: "4.jpeg",
      title: "Image 4",
    },
    {
      img: "5.jpeg",
      title: "Image 5",
    },
    {
      img: "6.jpeg",
      title: "Image 6",
    },
    {
      img: "7.jpeg",
      title: "Image 7",
    },
    {
      img: "8.jpeg",
      title: "Image 8",
    },
    {
      img: "9.jpeg",
      title: "Image 9",
    },
    {
      img: "10.jpeg",
      title: "Image 10",
    },
    {
      img: "11.jpeg",
      title: "Image 11",
    },
    {
      img: "12.jpeg",
      title: "Image 12",
    },
    {
      img: "13.jpeg",
      title: "Image 13",
    },
    {
      img: "14.jpeg",
      title: "Image 14",
    },
    {
      img: "15.jpeg",
      title: "Image 15",
    },
    {
      img: "16.jpeg",
      title: "Image 16",
    },
    {
      img: "17.jpeg",
      title: "Image 17",
    },
    {
      img: "18.jpeg",
      title: "Image 18",
    },
    {
      img: "19.jpeg",
      title: "Image 19",
    },
    {
      img: "20.jpeg",
      title: "Image 20",
    },
    {
      img: "21.jpeg",
      title: "Image 21",
    },
    {
      img: "22.jpeg",
      title: "Image 22",
    },
    {
      img: "23.jpeg",
      title: "Image 23",
    },
  ];

  return (
    <Box sx={{ p: 3, py: 2 }}>
      <ImageList
        sx={{ width: "50vw", height: "80vh" }}
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
              src={require(`../../../images/${item.img}`)} // Replace with your local image path
              alt={item.title}
              loading="lazy"
            />
          </ImageListItem>
        ))}
      </ImageList>
    </Box>
  );
};

export default ImageGrid;
