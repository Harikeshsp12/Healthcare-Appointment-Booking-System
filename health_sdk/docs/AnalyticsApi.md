# health_sdk.AnalyticsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_dashboard_stats**](AnalyticsApi.md#get_dashboard_stats) | **GET** /stats | Get Dashboard Stats


# **get_dashboard_stats**
> DashboardStatsResponse get_dashboard_stats()

Get Dashboard Stats

Get dashboard analytics for doctors and appointments.

### Example


```python
import health_sdk
from health_sdk.models.dashboard_stats_response import DashboardStatsResponse
from health_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = health_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with health_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = health_sdk.AnalyticsApi(api_client)

    try:
        # Get Dashboard Stats
        api_response = api_instance.get_dashboard_stats()
        print("The response of AnalyticsApi->get_dashboard_stats:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AnalyticsApi->get_dashboard_stats: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**DashboardStatsResponse**](DashboardStatsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

