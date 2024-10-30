import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from "./pages/Home"
import ProductFinder from './pages/ProductFinder';
import ProductCategorization from './pages/ProductCategorization';

function App() {
  return (
    <Router>
      <Routes>
        <Route path = "/" element = {<Home />}></Route>
        <Route path = "/ProductFinder" element = {<ProductFinder />} />
        <Route path = "/ProductCategorization" element = {<ProductCategorization />}></Route>
      </Routes>
    </Router>
  );
}

export default App;
