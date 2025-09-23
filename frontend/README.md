# Survey Management Frontend

React TypeScript frontend for the Survey Management System.

## Features

- Modern React 18 with TypeScript
- TailwindCSS for styling
- HeadlessUI for accessible components
- Heroicons for beautiful icons
- React Router for navigation
- Responsive design

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Build for production:
```bash
npm run build
```

## Available Scripts

- `npm start` - Runs the development server
- `npm run build` - Builds the app for production
- `npm test` - Runs the test suite
- `npm run eject` - Ejects from Create React App (one-way operation)

## Environment Variables

Create a `.env` file in the frontend directory:

```
REACT_APP_API_URL=http://localhost:8000/api
```

## Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/         # Page components
├── api.ts         # API client functions
├── types.ts       # TypeScript type definitions
├── App.tsx        # Main application component
└── index.tsx      # Application entry point
```
