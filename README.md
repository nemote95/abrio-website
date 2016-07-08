# AbrIO
Abrio is always there for you!

### Requirements
python 2.x

### How to run?
1. Go to project path
2. Create a virtual environment: `virtualenv venv`
alternative: if virtualenv haven't been installed use `sudo apt-get install virtual` to install it.
3. Go to created environment by `source venv/bin/activate`
4. Install project dependencies by `pip install -r requirments`
5. edit `environ.py.sample`, then rename it to `environ.py`
6. create database by `python manage.py database create`
7. Run project `python manage.py runserver`

### Database Commands:
1. to create database : `manage.py database create`
2. to drop database : `manage.py database drop`
3. to recreate database : `manage.py database recreate`
3. to generate fake data  : `manage.py database fake`
