# Cli-task-manager

A simple command-line application to manage personal and professional to-do lists. Built with Python, Click, and SQLite, this tool offers fast, reliable CRUD  operations and a user-friendly interface.
---
## Features
- Intialize a persistent SQLite database
- Add new tasks with title, description, due date, and priority
- List all tasks in a neatly formatted table
- Update tasks fields (title, description, due date, priority, status)
- Delete tasks by ID

  ---
  ## Installation
  1- Clone this repository:
     ```bash
     git clone https://github.com/luis-c2255/cli-task-manager.git
     ```
  2- Change into the project directory
     ```bash
     cd cli-task-manager
     ```
  3- Create and activate a virtual environment
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
  4- Install dependencies
     ```bash
     pip install -r requirements.txt
     ```
  ## Usage
  1- Initialize the database
     ```bash
     python cli.py init
     ```
  2- Add a task
     ```bash
     python cli.py add "Buy groceries" --description "Milk, eggs, bread" --due 20-10-2025 --priority 2
     ```
  3- List all tasks
     ```bash
     python cli.py list
     ```
  4- Update a task
     ```bash
     python cli.py update 1 --status done --priority 5
     ```
  5- Delete a task
     ```bash
     python cli.py delete 1
     ```
  ## Contributing
  Contributions are welcome. Please for the repository and open a pull request with your changes.

  ## License
  This project is licensed under the MIT License.
  See [LICENSE](https://LICENSE) for details.

  
