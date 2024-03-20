import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navigation from './components/Navigation/Navigation';
import Footer from './components/Footer/Footer'; // Import the Footer component
import Home from './pages/Home/Home';
import About from './pages/About/About';
import Classes from './pages/Classes/Classes';
import Events from './pages/Events/Events';
import Registration from './pages/Classes/Registration';

function App() {
  return (
    <Router>
      <Navigation />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/classes" element={<Classes />} />
        <Route path="/events" element={<Events />} />
        <Route path="/about" element={<About />} />
        <Route path="/register" element={<Registration />} />
      </Routes>
      <Footer /> {/* This is where the Footer is added */}
    </Router>
  );
}

export default App;
