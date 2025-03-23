# Chatbot Frontend

A beautiful and responsive chatbot interface built with React, TypeScript, and Tailwind CSS.

## Features

- Clean and modern UI
- Real-time message updates
- Loading states
- Auto-scrolling to latest messages
- Responsive design
- TypeScript for type safety

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn

## Setup

1. Install dependencies:
```bash
npm install
# or
yarn install
```

2. Start the development server:
```bash
npm start
# or
yarn start
```

The application will be available at `http://localhost:3000`.

## API Integration

This frontend expects a backend API running at `http://localhost:5000` with the following endpoint:

- POST `/chat`
  - Request body: `{ "message": "user message" }`
  - Response: `{ "response": "bot response" }`

Make sure your backend API is running and accessible at the specified URL before testing the chat interface. 