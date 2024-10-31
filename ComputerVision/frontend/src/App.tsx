import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Home, ProductFinder, ProductCategorization } from "./pages";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />}></Route>
        <Route path="/ProductFinder" element={<ProductFinder />} />
        <Route
          path="/ProductCategorization"
          element={<ProductCategorization />}
        ></Route>
      </Routes>
    </Router>
  );
}

export default App;
