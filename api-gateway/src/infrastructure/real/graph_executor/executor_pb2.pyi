from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExecutionRequest(_message.Message):
    __slots__ = ("query_text", "plan")
    QUERY_TEXT_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    query_text: str
    plan: RetrievalPlan
    def __init__(self, query_text: _Optional[str] = ..., plan: _Optional[_Union[RetrievalPlan, _Mapping]] = ...) -> None: ...

class RetrievalPlan(_message.Message):
    __slots__ = ("edges",)
    EDGES_FIELD_NUMBER: _ClassVar[int]
    edges: _containers.RepeatedCompositeFieldContainer[ToolEdge]
    def __init__(self, edges: _Optional[_Iterable[_Union[ToolEdge, _Mapping]]] = ...) -> None: ...

class ToolEdge(_message.Message):
    __slots__ = ("source", "to")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    source: str
    to: str
    def __init__(self, source: _Optional[str] = ..., to: _Optional[str] = ...) -> None: ...

class ExecutionResponse(_message.Message):
    __slots__ = ("context",)
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    context: Context
    def __init__(self, context: _Optional[_Union[Context, _Mapping]] = ...) -> None: ...

class Context(_message.Message):
    __slots__ = ("data",)
    class DataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.ScalarMap[str, str]
    def __init__(self, data: _Optional[_Mapping[str, str]] = ...) -> None: ...
