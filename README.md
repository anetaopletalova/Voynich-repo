# Running the API with database

To run this in a Docker container you need to install Docker and Python (I am using version 3.8.6)

Then in the project directory run these commands (will be simplified in the future)

```
docker-compose build

docker-compose up -d

docker-compose exec api python manage.py create_db

docker-compose exec api python manage.py seed_db

docker-compose exec api python manage.py import_data

docker-compose exec api python manage.py add_user [your username]
```

The last command will create your user with specified username and a default password 'password'
