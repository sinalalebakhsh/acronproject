docker-compose down

docker-compose up --build


# in another Terminal Page
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate







#  for ooveride .gitignore
git rm -r --cached .

