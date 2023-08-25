# Companies House API Connector

A brief example of how to connect to the Companies House API based on an article published for the ICAEW Data Analytics community.

## Set-up

You will need a Companies House API key, the instructions to obtain one can be found [here](https://developer.company-information.service.gov.uk/how-to-create-an-application).

Once obtained, this should be saved in a `.env` file under the `COH_API_KEY` key.

Install the packages from the `requirements.txt` file.

## Methods

### build_api_request

Main method for creating a request to a given endpoint. Takes the following arguments:

- `http_method`: the relevant HTTP method, e.g. GET
- `endpoint`: the Companies House API endpoint to send the request to
- `**kwargs`: arguments to pass to the `requests.Request` method

### get_request

Main method for a `GET` request to a given endpoint, and deals with pagination in the response. Takes the following arguments:

- `endpoint`: the Companies House API endpoint to send the request to

### get_officers

This method obtains details of all offices, past and present, for a given company. Takes the following arguments:

- `company_number`: the relevant company number

### get_directors

This method obtains all the active directors for a given company, returning them in a Pandas DataFrame for further analysis. Takes the following arguments:

- `company_number`: the relevant company number
