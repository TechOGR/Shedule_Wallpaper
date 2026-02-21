import React from "react";
import ReactDOM from "react-dom/client";

import { App } from "./App"


const elementRoot = document.getElementById("root");
const root = ReactDOM.createRoot(elementRoot)

root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
)
