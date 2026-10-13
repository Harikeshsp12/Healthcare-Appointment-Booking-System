# AppointmentResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**doctor_id** | **int** |  | 
**patient_name** | **str** |  | 
**slot** | **datetime** |  | 

## Example

```python
from health_sdk.models.appointment_response import AppointmentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AppointmentResponse from a JSON string
appointment_response_instance = AppointmentResponse.from_json(json)
# print the JSON string representation of the object
print(AppointmentResponse.to_json())

# convert the object into a dict
appointment_response_dict = appointment_response_instance.to_dict()
# create an instance of AppointmentResponse from a dict
appointment_response_from_dict = AppointmentResponse.from_dict(appointment_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


