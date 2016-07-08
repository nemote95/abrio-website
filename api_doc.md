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

4. Run a project

    URI : `<base_url>/api/v1/project/start`

    Method : POST

    Description : Start running  project

    Parameters :

	    Header {String} Content-Type=application/json JSON (application/json)
		Param {String}	private_key

5. Stop a running project

    URI : `<base_url>/api/v1/project/start`

    Method : POST

    Description : Stop a running  project

    Parameters :

	    Header {String} Content-Type=application/json JSON (application/json)
		Param {String}	private_key

6. Components list

    URI : `<base_url>/api/v1/project/component_list`

    Method : GET

    Description : Get list of components in a project

    Parameters :

	    Header {String} Content-Type=application/json JSON (application/json)
	    Param {String}	private_key

7. Project information

    URI : `<base_url>/api/v1/project/status`

    Method : GET

    Description : Get project info

    Parameters :

        Header {String} Content-Type=application/json JSON (application/json)
	    Param {String}	private_key

8. Remove a component

    URI : `<base_url>/api/v1/project/status`

    Method : DELETE

    Description : Remove a component if it's not used in a logic

    Parameters :

        Header {String}	private_key