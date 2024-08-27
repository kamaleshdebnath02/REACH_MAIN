import React from 'react';
import ReactDOM from 'react-dom';
import { createRoot } from 'react-dom/client';
import './index.css';  // Global styles specific to index if needed
import App from './App';
//import reportWebVitals from './reportWebVitals';  // This is optional and part of create-react-app

// If you are using a service worker:
//import * as serviceWorker from './serviceWorker';
const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

// Optional: Setup for service workers, if you are planning to make your app work offline or load faster
// serviceWorker.unregister(); // Change to register() if you want to use it

// Optional: This is for measuring performance during development
// reportWebVitals(console.log);
//serviceWorker.register();
