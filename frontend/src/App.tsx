import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">AI Chatbot</h1>
        <ChatInterface />
      </div>
    </div>
  );
}

export default App; 