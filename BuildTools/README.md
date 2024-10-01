# Moss usage

## Requirements
- [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/)

## Usage
Go to the BuildTools directory

Ensure that Docker Desktop is running by opening Docker Desktop from your Start menu

Open a Powershell Command Line (Powershell in your start menu)

Change to the directory where these files exist

Copy the `example.env_vars` and save it as `.env_vars`, and replace the placeholders with your own values

Start the docker containers

Create a language directory under assignments (ex: python)

Create an assignment directory under the language directory (ex: assignment1)

You should now have a directory to place the assignment files in

Copy the assignment files into the assignmentx directory.

Click on the plagiarims project in Docker Desktop and then click on the moss container

The logs of the moss container will be displayed in the Docker Desktop terminal.

The container will continue to run indefinitely until you stop it.

Any results from moss will be saved in the assignmentx directory.

There will be 3 files
- moss_m10.csv
- moss_m10.html
- moss_m10.results



### Stand up the containers
Run the following command to run moss
```powershell
docker compose -f .\BuildTools\docker-compose.yml up -d --force-recreate --remove-orphans --build
```

When looking at Docker Desktop you will now see the container running

### Stop containers
If you want to stop the containers, but plan on going back to use them later
```powershell
docker compose -f .\BuildTools\docker-compose.yml stop
```

### Start containers
If you want to start the containers after stopping them
```powershell
docker compose -f .\BuildTools\docker-compose.yml start
```

### Teardown containers
To remove the containers run this in powershell
```powershell
docker compose -f .\BuildTools\docker-compose.yml down
```
