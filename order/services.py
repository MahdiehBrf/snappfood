from typing import Optional

import requests

from order.api.serializers.third_party_serializers import MockResponseSerializer


def re_estimate_delivery_hour() -> Optional[int]:
    try:
        response = requests.get('https://run.mocky.io/v3/122c2796-5df4-461c-ab75-87c1192b17f7')
        json_response = response.json()
        serializer = MockResponseSerializer(data=json_response)
        serializer.is_valid(raise_exception=False)
    except requests.exceptions.ConnectionError:
        return
    validated_data = serializer.data
    if not validated_data["status"]:
        return
    return validated_data["data"]["eta"]
