import React from 'react';
import ChatInterface from './components/ChatInterface';
import logo from './logo.png';

function App() {
  return (
    <div className="min-h-screen bg-[#262f55]">
      <div className="border-2 border-[#fed34b] py-4 mb-2 bg-white/90">
        <div className="flex justify-center items-center">
          <img src={logo} alt="Logo" className="h-16 object-contain" />
        </div>
      </div>
      <ChatInterface />
    </div>
  );
}

export default App; 