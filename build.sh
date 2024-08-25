set -o errexit

pip install -r requirements.txt

python DjangoProyect/manage.py migrate
