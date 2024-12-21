## Getting Started:
### Prerequisites:
python>=3.12
uv>=0.5.10

### Project Setup:
1.Clone the project repository:
```bash
git clone git@github.com:Tad0k0/TestWork020.git
```
2.Select the directory of the project:
```bash
cd TestWork020
```
3. To launch the project locally, rename `.env_local_example` to `.env`. Uv will automatically create a virtual environment and install dependencies.
```bash
sudo docker-compose -f docker-compose-dev.yaml up -d
uv run alembic upgrade head 
uv run celery -A transaction.worker.c_worker worker --loglevel=INFO & uv run main.py
```
To launch the project using docker-compose, rename `.env_docker_example` to `.env`.
```bash
sudo docker-compose up -d
```
Change .env variables to local, and launch
```bash
uv run alembic upgrade head
```
Change .env variables to docker, and launch  
```bash
sudo docker-compose up -d
```