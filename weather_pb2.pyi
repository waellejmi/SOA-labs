from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CityRequest(_message.Message):
    __slots__ = ("city",)
    CITY_FIELD_NUMBER: _ClassVar[int]
    city: str
    def __init__(self, city: _Optional[str] = ...) -> None: ...

class TemperatureResponse(_message.Message):
    __slots__ = ("city", "temperature")
    CITY_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    city: str
    temperature: float
    def __init__(self, city: _Optional[str] = ..., temperature: _Optional[float] = ...) -> None: ...
