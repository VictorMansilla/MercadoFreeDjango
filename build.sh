set -o errexit

python.exe -m pip install --upgrade pip

pip install -r requirements.txt

python DjangoProyecto/manage.py migrate
