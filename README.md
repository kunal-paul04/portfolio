# Portfolio Project

This is a full-stack portfolio project built using **FastAPI** and **MongoDB** as the database. The portfolio is inspired by [Siddesh1210](https://github.com/Siddesh1210), with a unique background and theme to make it original.

## Project Structure (FastAPI)

The project is built using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python-type hints. It handles all API requests and interacts with a MongoDB database.

#### Folder Structure

portfolio/ 
├── app/ 
│ ├── __init__.py
│ ├── models.py 
│ ├── routes/ 
│ └── database.py 
├── main.py 
├── requirements.txt 
└── Dockerfile 


### Database (MongoDB)

MongoDB is used as the database to store portfolio items, contact messages, and other necessary data.

### Docker

Docker is used to containerize the application, making it easy to deploy and run on any environment.

## Getting Started

### Prerequisites

- Python 3.9+
- Docker
- MongoDB

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/portfolio-project.git
    cd portfolio-project
    ```


2. **Set up the environment variables:**
    Create a .env file in the portfolio-frontend directory and add the following:
    ```env
    REACT_APP_BACKEND_URL=http://localhost:8000
    ```

    Create a .env file in the portfolio-backend directory and add the following:
    ```env
    MONGO_DETAILS=mongodb://mongo:27017
    ```

3. **Run the application using Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    This command will build and start both the frontend and backend services along with MongoDB.

4. **Access the Application:**
    - Open http://localhost:8000 in your browser.

### Features
    - Fully responsive React frontend
    - FastAPI backend with MongoDB integration
    - CRUD operations for portfolio items
    - Contact form to collect messages
    - Dockerized for easy deployment

### Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or new features.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

### Contact
If you have any questions or feedback, please feel free to contact me at [kunalkantipaul@gmail.com].