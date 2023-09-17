import React, { useState, createContext } from "react";

import ImageGrid from "./ImageGrid/ImageGrid";
import KeyImage from "./KeyImage/KeyImage";

const SelectedImageContext = createContext();

const Gallery = () => {
  // Define the selectedImage state using useState
  const [selectedImage, setSelectedImage] = useState(null);
  return (
    <SelectedImageContext.Provider value={{ selectedImage, setSelectedImage }}>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "20px",
        }}
      >
        <ImageGrid />
        <KeyImage />
      </div>
    </SelectedImageContext.Provider>
  );
};

export default Gallery;

// You can also export the context for other components to use
export { SelectedImageContext };
