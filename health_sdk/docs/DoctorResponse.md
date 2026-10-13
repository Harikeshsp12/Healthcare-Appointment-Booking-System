# DoctorResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Doctor&#39;s full name | 
**specialization** | **str** | Medical specialization | 
**start_hour** | **int** | Shift start hour (0-23) | 
**end_hour** | **int** | Shift end hour (1-24) | 
**id** | **int** |  | 

## Example

```python
from health_sdk.models.doctor_response import DoctorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DoctorResponse from a JSON string
doctor_response_instance = DoctorResponse.from_json(json)
# print the JSON string representation of the object
print(DoctorResponse.to_json())

# convert the object into a dict
doctor_response_dict = doctor_response_instance.to_dict()
# create an instance of DoctorResponse from a dict
doctor_response_from_dict = DoctorResponse.from_dict(doctor_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


