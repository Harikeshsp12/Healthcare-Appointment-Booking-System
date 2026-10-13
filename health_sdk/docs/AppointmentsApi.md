# health_sdk.AppointmentsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**book_appointment**](AppointmentsApi.md#book_appointment) | **POST** /appointments/ | Book Appointment
[**cancel_appointment**](AppointmentsApi.md#cancel_appointment) | **DELETE** /appointments/{id} | Cancel Appointment
[**get_appointment_by_id**](AppointmentsApi.md#get_appointment_by_id) | **GET** /appointments/{id} | Get Appointment By Id
[**get_dashboard_stats**](AppointmentsApi.md#get_dashboard_stats) | **GET** /stats | Get Dashboard Stats
[**list_appointments**](AppointmentsApi.md#list_appointments) | **GET** /appointments/ | List Appointments


# **book_appointment**
> AppointmentResponse book_appointment(appointment_create)

Book Appointment

Book an appointment with a doctor.
Enforces:
1. Doctor must exist.
2. Appointment slot must be within the doctor's working hours.
3. Doctor cannot be double-booked for the same time slot.

### Example


```python
import health_sdk
from health_sdk.models.appointment_create import AppointmentCreate
from health_sdk.models.appointment_response import AppointmentResponse
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
    api_instance = health_sdk.AppointmentsApi(api_client)
    appointment_create = health_sdk.AppointmentCreate() # AppointmentCreate | 

    try:
        # Book Appointment
        api_response = api_instance.book_appointment(appointment_create)
        print("The response of AppointmentsApi->book_appointment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AppointmentsApi->book_appointment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **appointment_create** | [**AppointmentCreate**](AppointmentCreate.md)|  | 

### Return type

[**AppointmentResponse**](AppointmentResponse.md)

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

# **cancel_appointment**
> MessageResponse cancel_appointment(id)

Cancel Appointment

Cancel an existing appointment by ID.

### Example


```python
import health_sdk
from health_sdk.models.message_response import MessageResponse
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
    api_instance = health_sdk.AppointmentsApi(api_client)
    id = 56 # int | 

    try:
        # Cancel Appointment
        api_response = api_instance.cancel_appointment(id)
        print("The response of AppointmentsApi->cancel_appointment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AppointmentsApi->cancel_appointment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**MessageResponse**](MessageResponse.md)

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

# **get_appointment_by_id**
> AppointmentResponse get_appointment_by_id(id)

Get Appointment By Id

Get appointment by ID.

### Example


```python
import health_sdk
from health_sdk.models.appointment_response import AppointmentResponse
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
    api_instance = health_sdk.AppointmentsApi(api_client)
    id = 56 # int | 

    try:
        # Get Appointment By Id
        api_response = api_instance.get_appointment_by_id(id)
        print("The response of AppointmentsApi->get_appointment_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AppointmentsApi->get_appointment_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**AppointmentResponse**](AppointmentResponse.md)

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
    api_instance = health_sdk.AppointmentsApi(api_client)

    try:
        # Get Dashboard Stats
        api_response = api_instance.get_dashboard_stats()
        print("The response of AppointmentsApi->get_dashboard_stats:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AppointmentsApi->get_dashboard_stats: %s\n" % e)
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

# **list_appointments**
> List[AppointmentResponse] list_appointments(doctor_id=doctor_id, patient_name=patient_name)

List Appointments

List all appointments with optional filters.

### Example


```python
import health_sdk
from health_sdk.models.appointment_response import AppointmentResponse
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
    api_instance = health_sdk.AppointmentsApi(api_client)
    doctor_id = 56 # int | Filter by doctor ID (optional)
    patient_name = 'patient_name_example' # str | Filter by patient name (optional)

    try:
        # List Appointments
        api_response = api_instance.list_appointments(doctor_id=doctor_id, patient_name=patient_name)
        print("The response of AppointmentsApi->list_appointments:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AppointmentsApi->list_appointments: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doctor_id** | **int**| Filter by doctor ID | [optional] 
 **patient_name** | **str**| Filter by patient name | [optional] 

### Return type

[**List[AppointmentResponse]**](AppointmentResponse.md)

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

