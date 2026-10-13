# DoctorAvailabilityResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**doctor_id** | **int** |  | 
**doctor_name** | **str** |  | 
**specialization** | **str** |  | 
**var_date** | **str** |  | 
**working_hours** | **str** |  | 
**slots** | [**List[SlotAvailability]**](SlotAvailability.md) |  | 

## Example

```python
from health_sdk.models.doctor_availability_response import DoctorAvailabilityResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DoctorAvailabilityResponse from a JSON string
doctor_availability_response_instance = DoctorAvailabilityResponse.from_json(json)
# print the JSON string representation of the object
print(DoctorAvailabilityResponse.to_json())

# convert the object into a dict
doctor_availability_response_dict = doctor_availability_response_instance.to_dict()
# create an instance of DoctorAvailabilityResponse from a dict
doctor_availability_response_from_dict = DoctorAvailabilityResponse.from_dict(doctor_availability_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


