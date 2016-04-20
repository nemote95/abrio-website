# AbrIO
Abrio is always there for you!

### Requirments
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

### API Documents
####  version : 1
1. Create component:

    URI : `<base_url>/api/v1/component/create`
    
    Method : POST
    
    Description : creates new component by the giving name
    
    Parameters :

        Proxy-User USER:PASSWORD
	    Header {String} Content-Type=application/json JSON (application/json)
	    Param  {String} new component name

2. Upload Component

    URI : `<base_url>/api/v1/component/upload`

    Method : POST

    Description : Upload new component and change the deploy version

    Parameters :
    
	    Header {String} Content-Type=application/json JSON (application/json)
	    Header {String}	private_key
	    Header {String}	deploy_version
	    Param  {file} File to be uploaded

3. Define Logic In a Project

    URI : `<base_url>/api/v1/project/define_logic`

    Method : POST

    Description : Define new logic between components in projects

    Parameters :
    
	    Header {String} Content-Type=application/json JSON (application/json)
		Param {Int}	project_id
	    Param {Int}	component_1_id
	    Param {Int}	component_2_id
		Param {String}	message_type


