# Fetch Data Engineering Assignment #

## Steps followed by the steps in the assignment description:
1. Clone this repo.
```bash
git clone https://github.com/paridhi-parajuli/DataEngineeringAssignment.git
```

2. Go into the cloned repo.

3. Install libraries.
```bash
pip install -r requirements.txt
```
4. Start docker.
```bash
docker-compose up -d
```
5. Set the variables.
```code
USERNAME = "postgres"
PASSWORD = "postgres"
HOST = "httsp://localhost:5432"
DB = "postgres"
ENDPOINT_URL = " http://localhost:4566/000000000000"
QUEUE_NAME = "login-queue"

```
6. Run the program.
```bash
python main.py
```
7. Check if its done
```bash
psql -d postgres -U postgres -p 5432 -h localhost -W
```
