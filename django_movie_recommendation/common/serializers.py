from typing import Type

from common.models import BaseModel
from rest_framework import serializers


class BaseMeta:
    model = BaseModel
    exclude = (
        'created_at',
        'updated_at',
    )


def serialize_input_data(
    input_serializer: Type[serializers.Serializer],
    data: dict,
    partial: bool = False,
) -> dict | None:
    """Validate input data and returns validated one

    Args:
        input_serializer (Type[serializers.Serializer])
        data (dict): data with which build the Model object
        partial (bool): for partial updates (default to False)

    Raises:
        ValidationError: if serializer is not valid

    Returns:
        dict: validated data dict
    """
    serializer_instance = input_serializer(data=data, partial=partial)
    if serializer_instance.is_valid(raise_exception=True):
        return serializer_instance.data
