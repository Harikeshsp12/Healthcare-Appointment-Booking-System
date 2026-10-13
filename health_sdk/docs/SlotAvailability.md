# SlotAvailability


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**time** | **str** | Time string formatted as HH:00 | 
**slot_datetime** | **datetime** | Full datetime timestamp of slot | 
**is_available** | **bool** | True if slot is free for booking, False if booked | 

## Example

```python
from health_sdk.models.slot_availability import SlotAvailability

# TODO update the JSON string below
json = "{}"
# create an instance of SlotAvailability from a JSON string
slot_availability_instance = SlotAvailability.from_json(json)
# print the JSON string representation of the object
print(SlotAvailability.to_json())

# convert the object into a dict
slot_availability_dict = slot_availability_instance.to_dict()
# create an instance of SlotAvailability from a dict
slot_availability_from_dict = SlotAvailability.from_dict(slot_availability_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


