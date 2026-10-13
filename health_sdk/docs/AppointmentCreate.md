# AppointmentCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**doctor_id** | **int** | ID of the doctor | 
**patient_name** | **str** | Patient&#39;s full name | 
**slot** | **datetime** | Appointment slot timestamp in ISO format | 

## Example

```python
from health_sdk.models.appointment_create import AppointmentCreate

# TODO update the JSON string below
json = "{}"
# create an instance of AppointmentCreate from a JSON string
appointment_create_instance = AppointmentCreate.from_json(json)
# print the JSON string representation of the object
print(AppointmentCreate.to_json())

# convert the object into a dict
appointment_create_dict = appointment_create_instance.to_dict()
# create an instance of AppointmentCreate from a dict
appointment_create_from_dict = AppointmentCreate.from_dict(appointment_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


