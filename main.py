# module imports
import requests
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()  # load our .env file, now accessible through os.getenv


class CompaniesHouseAPI(object):
    def __init__(self, api_key: str) -> None:
        """Example class for housing all methods and attributes for connecting to the Companies House API

        Args:
            api_key (str): our API key
        """
        self.api_key = api_key  # set our API key
        self.base_url = "https://api.company-information.service.gov.uk/"  # base url, common across all requests

    def build_api_request(
        self, http_method: str, endpoint: str, **kwargs
    ) -> requests.Response:
        """Our method for building a general request to the API

        Args:
            http_method (str): relevant method, e.g. GET, POST, PUT etc
            endpoint (str): the endpoint to use

        Returns:
            requests.Response: returns a Response object
        """
        url = f"{self.base_url}{endpoint}"  # create the full request URL
        kwargs["headers"] = {"Authorization": self.api_key}  # set auth header
        # create our request
        r = requests.request(http_method, url, **kwargs)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()  # throws an error if request fails (see requests package documentation)

        return r

    def get_request(self, endpoint: str) -> dict:
        """Method for a GET request which also handles pagination for endpoints that return lists

        Args:
            endpoint (str): endpoint to use

        Returns:
            dict: JSON response
        """
        # create initial request and get JSON representation
        r = self.build_api_request("GET", endpoint).json()

        # check for pagination
        if "items_per_page" in r:
            items_per_page = r["items_per_page"]  # capture number per page
            start_index = 0  # first call will always be 0
            total_results = r["total_results"]  # total results to capture
            r = r["items"]  # r now holds our actual response data

            while (start_index + items_per_page) <= total_results:
                start_index += items_per_page  # i.e. move forward 1 page
                # build our next request with an updated start_index
                r_next = self.build_api_request(
                    "GET", endpoint, params={"start_index": start_index}
                )
                r.extend(r_next.json()["items"])  # combine our results

        return r

    def get_officers(self, company_number: str) -> dict:
        """Method to get all officers for a company

        Args:
            company_number (str): company number

        Returns:
            dict: JSON response containing all officers
        """
        endpoint = f"company/{company_number}/officers"  # construct our endpoint
        r = self.get_request(endpoint=endpoint)
        return r

    def get_directors(self, company_number: str) -> pd.DataFrame:
        """Method to obtain all active directors for a company and convert the information to a DataFrame.
        Returns just the Role, Appointment Date, Name and Link columns

        Args:
            company_number (str): company number

        Returns:
            pd.DataFrame: DataFrame of active directors
        """
        r = self.get_officers(company_number)  # all our officers
        df = pd.json_normalize(r)  # convert our json response to a DataFrame
        cols_to_keep = [
            "officer_role",
            "name",
            "appointed_on",
            "links.officer.appointments",
            "resigned_on",
        ]  # columns to keep
        df = df.drop(
            columns=list(set(df.columns) - set(cols_to_keep))
        )  # drop all other columns
        return (
            df.loc[(df["officer_role"] == "director") & (df["resigned_on"].isna())]
            .drop(columns="resigned_on")
            .reset_index(drop=True)
        )
