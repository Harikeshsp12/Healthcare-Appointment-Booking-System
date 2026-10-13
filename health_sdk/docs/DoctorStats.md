# DoctorStats


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**doctor_id** | **int** |  | 
**doctor_name** | **str** |  | 
**specialization** | **str** |  | 
**appointment_count** | **int** |  | 

## Example

```python
from health_sdk.models.doctor_stats import DoctorStats

# TODO update the JSON string below
json = "{}"
# create an instance of DoctorStats from a JSON string
doctor_stats_instance = DoctorStats.from_json(json)
# print the JSON string representation of the object
print(DoctorStats.to_json())

# convert the object into a dict
doctor_stats_dict = doctor_stats_instance.to_dict()
# create an instance of DoctorStats from a dict
doctor_stats_from_dict = DoctorStats.from_dict(doctor_stats_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


