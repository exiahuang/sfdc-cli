"""Simple-Salesforce Package"""
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from .myconsole import MyConsole

from .api import (
    Salesforce,
    SalesforceAPI,
    SFType,
    SalesforceError,
    SalesforceMoreThanOneRecord,
    SalesforceExpiredSession,
    SalesforceRefusedRequest,
    SalesforceResourceNotFound,
    SalesforceGeneralError,
    SalesforceMalformedRequest
)

from .login import (
    SalesforceLogin, SalesforceAuthenticationFailed
)


from .core import (
    Soap,
    MetadataApi,
    RestApi,
    ToolingApi,
    SoapException
)




from .bulk import Bulk
