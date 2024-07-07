# Flask API

This is a Flask API codebase that provides user management functionality.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo.git
    ```

2. Navigate to the project directory:

    ```bash
    cd user-management
    ```

3. Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```

4. Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

5. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```
6. Install Docker and Docker compose by following these instruction: 
    ```
    https://docs.docker.com/compose/install/
    https://docs.docker.com/engine/install/ubuntu/
    ```
## Usage

1. Running docker compose file
    ```bash
    docker-compose up -d
    ```

2. Access the API endpoints using the following base URL:

    ```
    http://localhost:8000
    ```

## API Endpoints

- `GET /users`: Get a list of all users(only for admins).
- `GET /users/profile`: Get details of a specific user.
- `POST /users/{user_id}/roles`:Add roles to users.
- `POST /auth/register`: Create a new user.
- `POST /auth/login`: Login.
- `POST /roles`: Create new Roles.
- `POST /roles/{role_id}/permissions`: Create or Add permission to roles.


## License

This project is licensed under the [MIT License](LICENSE).