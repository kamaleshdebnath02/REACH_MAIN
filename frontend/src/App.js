import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Chatbot from './components/Chatbot/Chatbot';
import Footer from './components/Footer';
import About from './components/About';  // Ensure this component exists
import Contact from './components/Contact';  // Ensure this component exists
import Dashboard from './components/Dashboard/Dashboard';  // Import Dashboard component
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Chatbot />} exact />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/dashboard" element={<Dashboard />} /> {/* Added route for Dashboard */}
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
