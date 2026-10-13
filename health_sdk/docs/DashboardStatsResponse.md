# DashboardStatsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_doctors** | **int** |  | 
**total_appointments** | **int** |  | 
**upcoming_appointments** | **int** |  | 
**doctor_stats** | [**List[DoctorStats]**](DoctorStats.md) |  | 

## Example

```python
from health_sdk.models.dashboard_stats_response import DashboardStatsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DashboardStatsResponse from a JSON string
dashboard_stats_response_instance = DashboardStatsResponse.from_json(json)
# print the JSON string representation of the object
print(DashboardStatsResponse.to_json())

# convert the object into a dict
dashboard_stats_response_dict = dashboard_stats_response_instance.to_dict()
# create an instance of DashboardStatsResponse from a dict
dashboard_stats_response_from_dict = DashboardStatsResponse.from_dict(dashboard_stats_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


