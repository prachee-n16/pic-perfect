import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import Gallery from "./components/SnapshotGallery/Gallery";
import Navbar from "./components/Navbar/Navbar";
import Footer from "./components/Footer/Footer";

const darkTheme = createTheme({
  palette: {
    mode: "dark",
    background: {
      default: "#000",
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Navbar />
      <Router>
        <Routes>
          <Route path="/" element={<Gallery />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
