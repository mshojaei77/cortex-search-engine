# Developer Guide: AI-Powered Personal Search Engine

This guide provides instructions for developers who want to edit, run, and contribute to the AI-Powered Personal Search Engine.

## 1. Project Overview

The search engine is built with a modern, decoupled architecture:

- **Frontend**: A React application built with TypeScript and Vite. It provides the user interface for searching and displaying results.
- **Backend (Metasearch)**: [SearXNG](https://docs.searxng.org/) is used as a privacy-respecting metasearch engine to aggregate results from various search providers.
- **AI Service**: An optional Python service using OpenAI's API to enhance search results with summaries, key points, and other insights.
- **Caching**: Redis is used to cache SearXNG results for improved performance.
- **Orchestration**: The entire application is containerized using Docker and managed with Docker Compose.

The frontend communicates with the SearXNG backend to fetch search results. If the AI service is enabled, the frontend can also call it to enhance the results.

## 2. Getting Started

Follow these steps to set up your local development environment.

### Prerequisites

- **Node.js**: Version 20 or higher.
- **Docker and Docker Compose**: Ensure they are installed and running.
- **OpenAI API Key**: Required if you want to use the AI enhancement features.

### Environment Setup

1.  **Clone the Repository**:
    ```bash
    git clone <your-repo-url>
    cd personal-search-engine
    ```

2.  **Create an Environment File**:
    Copy the example environment file to create your local configuration:
    ```bash
    cp .env.example .env
    ```

3.  **Configure Environment Variables**:
    Open the `.env` file and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    SEARXNG_HOSTNAME=localhost
    ```
    You can also customize the ports and other settings in this file.

## 3. Running the Application

You can run the application in two modes: with or without the AI service.

### Standard Mode (without AI)

This mode runs the frontend, SearXNG, and Redis.

1.  **Build and Start Services**:
    ```bash
    docker-compose up -d --build
    ```
    This command builds the Docker images and starts the services in detached mode.

2.  **Install Frontend Dependencies**:
    ```bash
    cd frontend
    npm install
    ```

3.  **Run the Frontend**:
    ```bash
    npm run dev
    ```

4.  **Access the Application**:
    Open your browser and navigate to `http://localhost:3000`.

### With AI Service

To run the application with AI-powered search enhancements, use the `with-ai` Docker Compose profile.

1.  **Build and Start All Services**:
    ```bash
    docker-compose --profile with-ai up -d --build
    ```

2.  **Install Frontend Dependencies and Run**:
    Follow the same steps as in the standard mode to install dependencies and run the frontend.

3.  **Access the Application**:
    The application will still be available at `http://localhost:3000`.

### Stopping the Application

To stop all running services, use the following command:
```bash
docker-compose down
```

## 4. Editing the Code

This section provides guidance on how to modify different parts of the application.

### Frontend (React + TypeScript)

-   **Location**: `frontend/`
-   **Key Files**:
    -   `src/App.tsx`: The main application component.
    -   `src/components/`: Reusable React components.
    -   `src/services/searchApi.ts`: Handles communication with the backend.
    -   `src/types/search.ts`: TypeScript type definitions.
-   **Development Workflow**:
    1.  Make sure the backend services (SearXNG, Redis) are running.
    2.  Navigate to the `frontend/` directory.
    3.  Run `npm run dev` to start the Vite development server with hot reloading.
    4.  Any changes you make to the source code will be reflected in your browser instantly.

### Backend (SearXNG)

-   **Location**: `backend/searxng/`
-   **Key File**:
    -   `settings.yml`: The main configuration file for SearXNG.
-   **Customization**:
    You can customize which search engines are used, the default language, and many other settings by editing `settings.yml`.
    -   To apply changes, you need to restart the `searxng` service:
        ```bash
        docker-compose restart searxng
        ```

### AI Service (OpenAI)

-   **Location**: `services/openai/`
-   **Key Files**:
    -   `main.py`: The main file for the FastAPI application.
    -   `client.py`: A client for interacting with the OpenAI API.
    -   `Dockerfile`: The Docker configuration for the service.
-   **Development Workflow**:
    1.  The AI service is a Python FastAPI application.
    2.  You can modify the code in `main.py` to change how search results are processed or to add new AI features.
    3.  To apply your changes, you'll need to rebuild the `openai-service` image:
        ```bash
        docker-compose --profile with-ai build openai-service
        ```
    4.  Then, restart the services:
        ```bash
        docker-compose --profile with-ai up -d
        ```

## 5. Troubleshooting

-   **`ECONNREFUSED` Error in the Frontend**:
    This usually means the SearXNG service is not running or is not accessible.
    -   Check if the Docker containers are running with `docker-compose ps`.
    -   Ensure that the `SEARXNG_HOSTNAME` and `SEARXNG_PORT` are correctly configured in your `.env` file and match the settings in `docker-compose.yml`.

-   **AI Features Not Working**:
    -   Make sure you are running the application with the `with-ai` profile.
    -   Verify that your `OPENAI_API_KEY` is correct in the `.env` file.
    -   Check the logs of the `openai-service` container for any errors:
        ```bash
        docker-compose logs openai-service
        ``` 