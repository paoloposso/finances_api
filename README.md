## Prepare Dev Environment and Dependencies

### Create virtual env

```
python -m venv venv
. ./venv/bin/activate
```

Alternatively you can use pipenv:

`pipenv shell` (with pipenv installed)

### Install dependencies
`pipenv sync --dev`

### Env vars
Create a `.env` file with the following content:

```bash
JWT_SECRET_KEY=random_value_6378632
MONGO_URL=mongodb://localhost:27017
MONGO_DATABASE_NAME=your_db_name
```

### Run database as container
If desired, you can run a mongo database as a container with the following command:
make db-start
Check the `makefile` in this repo for more commands that you can use to create and run the environment.

## Execute tests
On terminal, run `pytest -v`

The tests are currently within the folder `tests``, at the root of the project.

## Debugging tests

### On VS Code

Create launch.json file on .vscode folder with the following content:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Pytest: tests/auth/*",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/venv/bin/pytest",  // Path to your pytest executable
            "args": [
                "-v",
                // "tests"
            ],
            "cwd": "${workspaceFolder}",
            "env": {},
            "console": "integratedTerminal",
            "internalConsoleOptions": "neverOpen"
        }
    ]
}
```

You can specify the folder as exemplified with _tests_ (commented down).

## Running the API

On terminal, run the following command:

`flask run`