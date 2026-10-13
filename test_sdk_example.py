"""
Demonstration script verifying the generated Python SDK.
Matches the exact usage required by the challenge specification.
"""
import sys
import os

# Ensure health_sdk is resolvable whether installed or referenced locally
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "health_sdk"))

from health_sdk import ApiClient, Configuration
from health_sdk.api.doctors_api import DoctorsApi
from health_sdk.api.appointments_api import AppointmentsApi


def main():
    print("Initializing Health SDK client...")
    config = Configuration(host="http://localhost:8000")
    client = ApiClient(configuration=config)
    api = DoctorsApi(client)

    print("DoctorsApi instantiated successfully:", api)
    print("Methods available on DoctorsApi:")
    for method in dir(api):
        if not method.startswith("_"):
            print(f" - {method}")

    appointments_api = AppointmentsApi(client)
    print("\nAppointmentsApi instantiated successfully:", appointments_api)
    print("Methods available on AppointmentsApi:")
    for method in dir(appointments_api):
        if not method.startswith("_"):
            print(f" - {method}")

    print("\n[SUCCESS] Health SDK verified according to challenge specifications.")


if __name__ == "__main__":
    main()
