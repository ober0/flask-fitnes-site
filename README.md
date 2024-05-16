# Client and Visit Management Web Application

This project is a web application for managing clients and their visits to a fitness club. It uses Flask as the web framework and SQLAlchemy for interacting with a SQLite database.

## Installation

1. Clone the repository:

    ```bash
    git clone <Repository>
    ```

2. Navigate to the project directory:

    ```bash
    cd your_project
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the application:

    ```bash
    python main.py
    ```

2. Open a web browser and go to `http://127.0.0.1:5000/` to access the application.

## Usage

### Adding a New Client

1. Go to the application's main page.

2. Click the "New Client" button.

3. Enter the new client's details and click the "Add" button.

### Editing Client Information

1. On the main page, find the client you want to edit.

2. Click the "Edit" button next to their details.

3. Make the necessary changes and click the "Save" button.

### Registering a Client's Visit

1. On the main page, find the client you want to check in.

2. Enter their locker number and click the "Check In" button.

3. The client will be marked as present, and their information will be updated.

### Viewing Clients and Visits

1. On the main page, you can see a list of all clients.

2. You can also view visits for a specific date or all-time visits.

### Adding a New Employee

1. Go to the "Add Employee" page.

2. Enter the new employee's details and click the "Add" button.

### Deleting an Employee

1. Go to the "Delete Employee" page.

2. Select the employee from the list and click the "Delete" button.

3. Confirm the deletion in the dialog box.

### Editing Employee Information

1. Go to the "Edit Employee Information" page.

2. Select the employee from the list and make the necessary changes.

3. Click the "Save" button.

### Viewing Employees

1. On the main page, you can see a list of all employees.

2. You can also view detailed information about each employee.

### View expiring subscriptions

1. Go to the "View order account" page.
2. The page will display subscriptions in the form of a table that expire in the next 30 days

## Author

- tg: Oberrrr
- ds: ober0

## License

This project is licensed under the [LICENSE](LICENSE).
