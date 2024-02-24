> Level: Easy.


Azure Client API 
--

Create Azure Client API CLI using `httpx` for GET/POST RestAPI operation.

- all needed data: 
    - https://learn.microsoft.com/en-us/rest/api/azure/devops/?view=azure-devops-rest-7.2
    - https://learn.microsoft.com/en-us/rest/api/azure/devops/core/projects?view=azure-devops-rest-7.2
    - https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items?view=azure-devops-rest-7.2
    - https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/wiql?view=azure-devops-rest-7.2
    - https://www.python-httpx.org/
    - https://www.python-httpx.org/async/

Phase 1: Pyhton CLI API
--
**OOP IS MUST**
* Use OOP concepts to structure and write these classes.
* Authorization:
  * Get API token from Azure DevOps RestAPI
  * Create a configuration file `settings.ini` and store the key there.
  * Read the key from the config file and do the authorization at the beginning of the program.
  * Use DataClasses to store the settings & Error & Success Respones.

* CLI: Using Sync Httpx
  * Show welcome message and list of operations. 
  * Create/List/Get/Delete Azure Project.
    * if user chooses to create will need to provide a project name.
    * if user chooses List will need to list all Azure projects for the user.
    * if user chooses get will need to list info about the project and list a new list of operations.
  
  * Create/List/Update/Get/Delete Work items:
    * Create a work items ( Task, Bug, ...) for the selected project.
    * https://learn.microsoft.com/en-us/rest/api/azure/devops/processes/work-item-types/list?view=azure-devops-rest-6.0&tabs=HTTP
    * List all work items for the selected project.
    * Update an item.
    * Delete an item.
    * Get an item.


   * Optional:
      *   copy/move/replace an item.

Phase 2: Pyhton CLI API With Async httpx client.
--

  * Write the same program with Httpx Async call and utilize it using asyncio or anyio.
  * User Must choose which client wants to run when the CLI App starts.

Phase 3: Telegram Bot API.
--

* send a notification on every op.

Side Task:
--

* Read and understand LZ77 Algo ( Must )
* XSS ( Must ).


Required Files.
-- 
These files are required for all Future tasks as well.

* Unit-Testing ( pytest ).
* PyDoc3
* Pylint
* venv
* requirements.txt
* __init__.py files
