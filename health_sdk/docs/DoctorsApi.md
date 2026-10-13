# health_sdk.DoctorsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_doctor**](DoctorsApi.md#add_doctor) | **POST** /doctors/ | Add Doctor
[**get_doctor_availability**](DoctorsApi.md#get_doctor_availability) | **GET** /doctors/{id}/availability | Get Doctor Availability
[**get_doctor_by_id**](DoctorsApi.md#get_doctor_by_id) | **GET** /doctors/{id} | Get Doctor By Id
[**list_doctors**](DoctorsApi.md#list_doctors) | **GET** /doctors/ | List Doctors


# **add_doctor**
> DoctorResponse add_doctor(doctor_create)

Add Doctor

Add a new doctor with their working hours.

### Example


```python
import health_sdk
from health_sdk.models.doctor_create import DoctorCreate
from health_sdk.models.doctor_response import DoctorResponse
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
    api_instance = health_sdk.DoctorsApi(api_client)
    doctor_create = health_sdk.DoctorCreate() # DoctorCreate | 

    try:
        # Add Doctor
        api_response = api_instance.add_doctor(doctor_create)
        print("The response of DoctorsApi->add_doctor:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DoctorsApi->add_doctor: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doctor_create** | [**DoctorCreate**](DoctorCreate.md)|  | 

### Return type

[**DoctorResponse**](DoctorResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_doctor_availability**
> DoctorAvailabilityResponse get_doctor_availability(id, query_date=query_date)

Get Doctor Availability

Get all 1-hour time slots and their availability for a specific doctor on a chosen date.

### Example


```python
import health_sdk
from health_sdk.models.doctor_availability_response import DoctorAvailabilityResponse
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
    api_instance = health_sdk.DoctorsApi(api_client)
    id = 56 # int | 
    query_date = 'query_date_example' # str | Date in YYYY-MM-DD format, defaults to today (optional)

    try:
        # Get Doctor Availability
        api_response = api_instance.get_doctor_availability(id, query_date=query_date)
        print("The response of DoctorsApi->get_doctor_availability:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DoctorsApi->get_doctor_availability: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 
 **query_date** | **str**| Date in YYYY-MM-DD format, defaults to today | [optional] 

### Return type

[**DoctorAvailabilityResponse**](DoctorAvailabilityResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_doctor_by_id**
> DoctorResponse get_doctor_by_id(id)

Get Doctor By Id

Get doctor details by ID.

### Example


```python
import health_sdk
from health_sdk.models.doctor_response import DoctorResponse
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
    api_instance = health_sdk.DoctorsApi(api_client)
    id = 56 # int | 

    try:
        # Get Doctor By Id
        api_response = api_instance.get_doctor_by_id(id)
        print("The response of DoctorsApi->get_doctor_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DoctorsApi->get_doctor_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**DoctorResponse**](DoctorResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_doctors**
> List[DoctorResponse] list_doctors()

List Doctors

List all registered doctors.

### Example


```python
import health_sdk
from health_sdk.models.doctor_response import DoctorResponse
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
    api_instance = health_sdk.DoctorsApi(api_client)

    try:
        # List Doctors
        api_response = api_instance.list_doctors()
        print("The response of DoctorsApi->list_doctors:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DoctorsApi->list_doctors: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[DoctorResponse]**](DoctorResponse.md)

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

