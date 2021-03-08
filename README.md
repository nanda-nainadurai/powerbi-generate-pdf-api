# Python Script to Generate PDF using REST APIs

You can directly follow the steps from [Microsoft docs](https://docs.microsoft.com/en-us/power-bi/developer/embedded/embed-service-principal) or follow the below instructions:

## Pre-requisites
1. Get Azure Tenant ID ([How to get](https://docs.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-how-to-find-tenant))
2. Register an app in Azure ([Using Azure Portal](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app), [Using PowerShell](https://docs.microsoft.com/en-us/power-bi/developer/embedded/embed-service-principal#creating-an-azure-ad-app-using-powershell) is recommended)
3. Create & Get Client Secret from [Azure Portal](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#option-2-create-a-new-application-secret) (HINT: You get access to your client secret only once, at the time of creation - so take a copy of it somewhere safe)
4. Get Client ID (for the app created in Step 2)
5. Ensure appropriate access is provided to the created service principal. In this case, the required scopes are the following:
- Report.ReadWrite.All or Report.Read.All
- Dataset.ReadWrite.All or Dataset.Read.All
6. The workspace must be created in Power BI Premium or Power BI Embedded Capacity for the API's to work (otherwise, you will get 403 errors while executing code)
7. [IMPORTANT] Enable the [Power BI service admin settings](https://docs.microsoft.com/en-us/power-bi/developer/embedded/embed-service-principal#step-3---enable-the-power-bi-service-admin-settings) for the service principal or the security group created in Step 5

## How to use
1. Clone the repository or download the "GeneratePDF.py" file and "data.json" file
2. Update the data.json file based on values gathere from the pre-requisites section
3. Open command prompt and run the command <code>python GeneratePDF.py</code>

## How it works!
1. A REST API is called to authenticate & authorize using the <code>CLIENT ID</code> and <code>CLIENT SECRET</code> that was added in the <code>data.json</code> file. This returns an authentication token ([for the curious](https://docs.microsoft.com/en-us/azure/architecture/multitenant-identity/client-assertion)) that will be used in subsequent REST API calls
2. [Export to File in Group](https://docs.microsoft.com/en-us/rest/api/power-bi/reports/exporttofileingroup) API is called to initiate the generation of file (PDF is passed as the parameter) and returns an id to track the status of the job
3. After trigger the job, use [polling](https://docs.microsoft.com/en-us/rest/api/power-bi/reports/getexporttofilestatus) to track the job until it is completed
4. Once the poll returns job status as success, [get the file of export](https://docs.microsoft.com/en-us/rest/api/power-bi/reports/getfileofexporttofile) from the server
5. This file is then saved local to the execution of the code

### Things to Note
1. The REST APIs are still in public preview and can sometimes behave unexpectedly
2. There are some known limitations captured in [this official link](https://docs.microsoft.com/en-us/power-bi/developer/embedded/export-to#limitations)

## Contributions
Feel free to contribute to the repository by raising issues or by creating Pull requests for any code/documentation updates.
