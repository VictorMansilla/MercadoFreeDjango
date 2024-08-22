set -o errexit

pip install -r requirements.txt

python DjangoProyecto/manage.py migrate
