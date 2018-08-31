#!/bin/bash

# Get the full path to this script, the top dir is one up.
TOPDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TOPDIR+=/..
cd $TOPDIR

rm -fr venv
virtualenv -p python3.6 venv
source venv/bin/activate
./scripts/cache_pip_packages.sh
pip install -f venv/pip_cache -r requirements.txt -t venv/packages

echo 'Creating our internal postgres application account...'
if [[ "$OSTYPE" == "linux"* ]]; then
  sudo -u postgres psql -c "CREATE USER openag WITH PASSWORD 'openag';"
  sudo -u postgres psql -c "ALTER USER openag SUPERUSER;"
  sudo -u postgres psql -c "CREATE DATABASE openag_brain OWNER openag;"
else # we are on OSX
  psql postgres -c "CREATE USER openag WITH PASSWORD 'openag';"
  psql postgres -c "ALTER USER openag SUPERUSER;"
  psql postgres -c "CREATE DATABASE openag_brain OWNER openag;"
fi

echo 'Creating the django/postgres database...'
python manage.py migrate

echo 'Creating the django/postgres admin account...'
#python manage.py createsuperuser
# The above command is interactive, the one below creates an openag / openag
# super user account without prompting:
echo "from django.contrib.auth.models import User; User.objects.filter(email='openag@openag.edu').delete(); User.objects.create_superuser('openag', 'openag@openag.edu', 'openag')" | python manage.py shell


# How to list the databases:
# psql --username=openag openag_brain -c '\l'

# How to list the tables in our database:
# psql --username=openag openag_brain -c '\dt'

# How to log into postgres interactively:
# psql --username=openag openag_brain 

