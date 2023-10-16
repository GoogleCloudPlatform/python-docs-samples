from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    Empty: _ClassVar[StatusCode]
    Continue: _ClassVar[StatusCode]
    OK: _ClassVar[StatusCode]
    Created: _ClassVar[StatusCode]
    Accepted: _ClassVar[StatusCode]
    NonAuthoritativeInformation: _ClassVar[StatusCode]
    NoContent: _ClassVar[StatusCode]
    ResetContent: _ClassVar[StatusCode]
    PartialContent: _ClassVar[StatusCode]
    MultiStatus: _ClassVar[StatusCode]
    AlreadyReported: _ClassVar[StatusCode]
    IMUsed: _ClassVar[StatusCode]
    MultipleChoices: _ClassVar[StatusCode]
    MovedPermanently: _ClassVar[StatusCode]
    Found: _ClassVar[StatusCode]
    SeeOther: _ClassVar[StatusCode]
    NotModified: _ClassVar[StatusCode]
    UseProxy: _ClassVar[StatusCode]
    TemporaryRedirect: _ClassVar[StatusCode]
    PermanentRedirect: _ClassVar[StatusCode]
    BadRequest: _ClassVar[StatusCode]
    Unauthorized: _ClassVar[StatusCode]
    PaymentRequired: _ClassVar[StatusCode]
    Forbidden: _ClassVar[StatusCode]
    NotFound: _ClassVar[StatusCode]
    MethodNotAllowed: _ClassVar[StatusCode]
    NotAcceptable: _ClassVar[StatusCode]
    ProxyAuthenticationRequired: _ClassVar[StatusCode]
    RequestTimeout: _ClassVar[StatusCode]
    Conflict: _ClassVar[StatusCode]
    Gone: _ClassVar[StatusCode]
    LengthRequired: _ClassVar[StatusCode]
    PreconditionFailed: _ClassVar[StatusCode]
    PayloadTooLarge: _ClassVar[StatusCode]
    URITooLong: _ClassVar[StatusCode]
    UnsupportedMediaType: _ClassVar[StatusCode]
    RangeNotSatisfiable: _ClassVar[StatusCode]
    ExpectationFailed: _ClassVar[StatusCode]
    MisdirectedRequest: _ClassVar[StatusCode]
    UnprocessableEntity: _ClassVar[StatusCode]
    Locked: _ClassVar[StatusCode]
    FailedDependency: _ClassVar[StatusCode]
    UpgradeRequired: _ClassVar[StatusCode]
    PreconditionRequired: _ClassVar[StatusCode]
    TooManyRequests: _ClassVar[StatusCode]
    RequestHeaderFieldsTooLarge: _ClassVar[StatusCode]
    InternalServerError: _ClassVar[StatusCode]
    NotImplemented: _ClassVar[StatusCode]
    BadGateway: _ClassVar[StatusCode]
    ServiceUnavailable: _ClassVar[StatusCode]
    GatewayTimeout: _ClassVar[StatusCode]
    HTTPVersionNotSupported: _ClassVar[StatusCode]
    VariantAlsoNegotiates: _ClassVar[StatusCode]
    InsufficientStorage: _ClassVar[StatusCode]
    LoopDetected: _ClassVar[StatusCode]
    NotExtended: _ClassVar[StatusCode]
    NetworkAuthenticationRequired: _ClassVar[StatusCode]
Empty: StatusCode
Continue: StatusCode
OK: StatusCode
Created: StatusCode
Accepted: StatusCode
NonAuthoritativeInformation: StatusCode
NoContent: StatusCode
ResetContent: StatusCode
PartialContent: StatusCode
MultiStatus: StatusCode
AlreadyReported: StatusCode
IMUsed: StatusCode
MultipleChoices: StatusCode
MovedPermanently: StatusCode
Found: StatusCode
SeeOther: StatusCode
NotModified: StatusCode
UseProxy: StatusCode
TemporaryRedirect: StatusCode
PermanentRedirect: StatusCode
BadRequest: StatusCode
Unauthorized: StatusCode
PaymentRequired: StatusCode
Forbidden: StatusCode
NotFound: StatusCode
MethodNotAllowed: StatusCode
NotAcceptable: StatusCode
ProxyAuthenticationRequired: StatusCode
RequestTimeout: StatusCode
Conflict: StatusCode
Gone: StatusCode
LengthRequired: StatusCode
PreconditionFailed: StatusCode
PayloadTooLarge: StatusCode
URITooLong: StatusCode
UnsupportedMediaType: StatusCode
RangeNotSatisfiable: StatusCode
ExpectationFailed: StatusCode
MisdirectedRequest: StatusCode
UnprocessableEntity: StatusCode
Locked: StatusCode
FailedDependency: StatusCode
UpgradeRequired: StatusCode
PreconditionRequired: StatusCode
TooManyRequests: StatusCode
RequestHeaderFieldsTooLarge: StatusCode
InternalServerError: StatusCode
NotImplemented: StatusCode
BadGateway: StatusCode
ServiceUnavailable: StatusCode
GatewayTimeout: StatusCode
HTTPVersionNotSupported: StatusCode
VariantAlsoNegotiates: StatusCode
InsufficientStorage: StatusCode
LoopDetected: StatusCode
NotExtended: StatusCode
NetworkAuthenticationRequired: StatusCode

class ProcessingRequest(_message.Message):
    __slots__ = ["async_mode", "request_headers", "response_headers", "request_body", "response_body", "request_trailers", "response_trailers"]
    ASYNC_MODE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_HEADERS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_HEADERS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_BODY_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_BODY_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TRAILERS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TRAILERS_FIELD_NUMBER: _ClassVar[int]
    async_mode: bool
    request_headers: HttpHeaders
    response_headers: HttpHeaders
    request_body: HttpBody
    response_body: HttpBody
    request_trailers: HttpTrailers
    response_trailers: HttpTrailers
    def __init__(self, async_mode: bool = ..., request_headers: _Optional[_Union[HttpHeaders, _Mapping]] = ..., response_headers: _Optional[_Union[HttpHeaders, _Mapping]] = ..., request_body: _Optional[_Union[HttpBody, _Mapping]] = ..., response_body: _Optional[_Union[HttpBody, _Mapping]] = ..., request_trailers: _Optional[_Union[HttpTrailers, _Mapping]] = ..., response_trailers: _Optional[_Union[HttpTrailers, _Mapping]] = ...) -> None: ...

class ProcessingResponse(_message.Message):
    __slots__ = ["request_headers", "response_headers", "request_body", "response_body", "request_trailers", "response_trailers", "immediate_response", "dynamic_metadata", "mode_override", "override_message_timeout"]
    REQUEST_HEADERS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_HEADERS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_BODY_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_BODY_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TRAILERS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TRAILERS_FIELD_NUMBER: _ClassVar[int]
    IMMEDIATE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    DYNAMIC_METADATA_FIELD_NUMBER: _ClassVar[int]
    MODE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_MESSAGE_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    request_headers: HeadersResponse
    response_headers: HeadersResponse
    request_body: BodyResponse
    response_body: BodyResponse
    request_trailers: TrailersResponse
    response_trailers: TrailersResponse
    immediate_response: ImmediateResponse
    dynamic_metadata: _struct_pb2.Struct
    mode_override: ProcessingMode
    override_message_timeout: _duration_pb2.Duration
    def __init__(self, request_headers: _Optional[_Union[HeadersResponse, _Mapping]] = ..., response_headers: _Optional[_Union[HeadersResponse, _Mapping]] = ..., request_body: _Optional[_Union[BodyResponse, _Mapping]] = ..., response_body: _Optional[_Union[BodyResponse, _Mapping]] = ..., request_trailers: _Optional[_Union[TrailersResponse, _Mapping]] = ..., response_trailers: _Optional[_Union[TrailersResponse, _Mapping]] = ..., immediate_response: _Optional[_Union[ImmediateResponse, _Mapping]] = ..., dynamic_metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., mode_override: _Optional[_Union[ProcessingMode, _Mapping]] = ..., override_message_timeout: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class HttpHeaders(_message.Message):
    __slots__ = ["headers", "attributes", "end_of_stream"]
    class AttributesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Struct
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    END_OF_STREAM_FIELD_NUMBER: _ClassVar[int]
    headers: HeaderMap
    attributes: _containers.MessageMap[str, _struct_pb2.Struct]
    end_of_stream: bool
    def __init__(self, headers: _Optional[_Union[HeaderMap, _Mapping]] = ..., attributes: _Optional[_Mapping[str, _struct_pb2.Struct]] = ..., end_of_stream: bool = ...) -> None: ...

class HttpBody(_message.Message):
    __slots__ = ["body", "end_of_stream"]
    BODY_FIELD_NUMBER: _ClassVar[int]
    END_OF_STREAM_FIELD_NUMBER: _ClassVar[int]
    body: bytes
    end_of_stream: bool
    def __init__(self, body: _Optional[bytes] = ..., end_of_stream: bool = ...) -> None: ...

class HttpTrailers(_message.Message):
    __slots__ = ["trailers"]
    TRAILERS_FIELD_NUMBER: _ClassVar[int]
    trailers: HeaderMap
    def __init__(self, trailers: _Optional[_Union[HeaderMap, _Mapping]] = ...) -> None: ...

class HeadersResponse(_message.Message):
    __slots__ = ["response"]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CommonResponse
    def __init__(self, response: _Optional[_Union[CommonResponse, _Mapping]] = ...) -> None: ...

class TrailersResponse(_message.Message):
    __slots__ = ["header_mutation"]
    HEADER_MUTATION_FIELD_NUMBER: _ClassVar[int]
    header_mutation: HeaderMutation
    def __init__(self, header_mutation: _Optional[_Union[HeaderMutation, _Mapping]] = ...) -> None: ...

class BodyResponse(_message.Message):
    __slots__ = ["response"]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CommonResponse
    def __init__(self, response: _Optional[_Union[CommonResponse, _Mapping]] = ...) -> None: ...

class CommonResponse(_message.Message):
    __slots__ = ["status", "header_mutation", "body_mutation", "trailers", "clear_route_cache"]
    class ResponseStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        CONTINUE: _ClassVar[CommonResponse.ResponseStatus]
        CONTINUE_AND_REPLACE: _ClassVar[CommonResponse.ResponseStatus]
    CONTINUE: CommonResponse.ResponseStatus
    CONTINUE_AND_REPLACE: CommonResponse.ResponseStatus
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HEADER_MUTATION_FIELD_NUMBER: _ClassVar[int]
    BODY_MUTATION_FIELD_NUMBER: _ClassVar[int]
    TRAILERS_FIELD_NUMBER: _ClassVar[int]
    CLEAR_ROUTE_CACHE_FIELD_NUMBER: _ClassVar[int]
    status: CommonResponse.ResponseStatus
    header_mutation: HeaderMutation
    body_mutation: BodyMutation
    trailers: HeaderMap
    clear_route_cache: bool
    def __init__(self, status: _Optional[_Union[CommonResponse.ResponseStatus, str]] = ..., header_mutation: _Optional[_Union[HeaderMutation, _Mapping]] = ..., body_mutation: _Optional[_Union[BodyMutation, _Mapping]] = ..., trailers: _Optional[_Union[HeaderMap, _Mapping]] = ..., clear_route_cache: bool = ...) -> None: ...

class ImmediateResponse(_message.Message):
    __slots__ = ["status", "headers", "body", "grpc_status", "details"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    GRPC_STATUS_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    status: HttpStatus
    headers: HeaderMutation
    body: str
    grpc_status: GrpcStatus
    details: str
    def __init__(self, status: _Optional[_Union[HttpStatus, _Mapping]] = ..., headers: _Optional[_Union[HeaderMutation, _Mapping]] = ..., body: _Optional[str] = ..., grpc_status: _Optional[_Union[GrpcStatus, _Mapping]] = ..., details: _Optional[str] = ...) -> None: ...

class GrpcStatus(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: int
    def __init__(self, status: _Optional[int] = ...) -> None: ...

class HeaderMutation(_message.Message):
    __slots__ = ["set_headers", "remove_headers"]
    SET_HEADERS_FIELD_NUMBER: _ClassVar[int]
    REMOVE_HEADERS_FIELD_NUMBER: _ClassVar[int]
    set_headers: _containers.RepeatedCompositeFieldContainer[HeaderValueOption]
    remove_headers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, set_headers: _Optional[_Iterable[_Union[HeaderValueOption, _Mapping]]] = ..., remove_headers: _Optional[_Iterable[str]] = ...) -> None: ...

class BodyMutation(_message.Message):
    __slots__ = ["body", "clear_body"]
    BODY_FIELD_NUMBER: _ClassVar[int]
    CLEAR_BODY_FIELD_NUMBER: _ClassVar[int]
    body: bytes
    clear_body: bool
    def __init__(self, body: _Optional[bytes] = ..., clear_body: bool = ...) -> None: ...

class HeaderMap(_message.Message):
    __slots__ = ["headers"]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    headers: _containers.RepeatedCompositeFieldContainer[HeaderValue]
    def __init__(self, headers: _Optional[_Iterable[_Union[HeaderValue, _Mapping]]] = ...) -> None: ...

class HeaderValue(_message.Message):
    __slots__ = ["key", "value", "raw_value"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    RAW_VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    raw_value: bytes
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ..., raw_value: _Optional[bytes] = ...) -> None: ...

class HeaderValueOption(_message.Message):
    __slots__ = ["header", "append", "append_action", "keep_empty_value"]
    class HeaderAppendAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        APPEND_IF_EXISTS_OR_ADD: _ClassVar[HeaderValueOption.HeaderAppendAction]
        ADD_IF_ABSENT: _ClassVar[HeaderValueOption.HeaderAppendAction]
        OVERWRITE_IF_EXISTS_OR_ADD: _ClassVar[HeaderValueOption.HeaderAppendAction]
        OVERWRITE_IF_EXISTS: _ClassVar[HeaderValueOption.HeaderAppendAction]
    APPEND_IF_EXISTS_OR_ADD: HeaderValueOption.HeaderAppendAction
    ADD_IF_ABSENT: HeaderValueOption.HeaderAppendAction
    OVERWRITE_IF_EXISTS_OR_ADD: HeaderValueOption.HeaderAppendAction
    OVERWRITE_IF_EXISTS: HeaderValueOption.HeaderAppendAction
    HEADER_FIELD_NUMBER: _ClassVar[int]
    APPEND_FIELD_NUMBER: _ClassVar[int]
    APPEND_ACTION_FIELD_NUMBER: _ClassVar[int]
    KEEP_EMPTY_VALUE_FIELD_NUMBER: _ClassVar[int]
    header: HeaderValue
    append: _wrappers_pb2.BoolValue
    append_action: HeaderValueOption.HeaderAppendAction
    keep_empty_value: bool
    def __init__(self, header: _Optional[_Union[HeaderValue, _Mapping]] = ..., append: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., append_action: _Optional[_Union[HeaderValueOption.HeaderAppendAction, str]] = ..., keep_empty_value: bool = ...) -> None: ...

class ProcessingMode(_message.Message):
    __slots__ = ["request_header_mode", "response_header_mode", "request_body_mode", "response_body_mode", "request_trailer_mode", "response_trailer_mode"]
    class HeaderSendMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        DEFAULT: _ClassVar[ProcessingMode.HeaderSendMode]
        SEND: _ClassVar[ProcessingMode.HeaderSendMode]
        SKIP: _ClassVar[ProcessingMode.HeaderSendMode]
    DEFAULT: ProcessingMode.HeaderSendMode
    SEND: ProcessingMode.HeaderSendMode
    SKIP: ProcessingMode.HeaderSendMode
    class BodySendMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        NONE: _ClassVar[ProcessingMode.BodySendMode]
        STREAMED: _ClassVar[ProcessingMode.BodySendMode]
        BUFFERED: _ClassVar[ProcessingMode.BodySendMode]
        BUFFERED_PARTIAL: _ClassVar[ProcessingMode.BodySendMode]
    NONE: ProcessingMode.BodySendMode
    STREAMED: ProcessingMode.BodySendMode
    BUFFERED: ProcessingMode.BodySendMode
    BUFFERED_PARTIAL: ProcessingMode.BodySendMode
    REQUEST_HEADER_MODE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_HEADER_MODE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_BODY_MODE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_BODY_MODE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TRAILER_MODE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TRAILER_MODE_FIELD_NUMBER: _ClassVar[int]
    request_header_mode: ProcessingMode.HeaderSendMode
    response_header_mode: ProcessingMode.HeaderSendMode
    request_body_mode: ProcessingMode.BodySendMode
    response_body_mode: ProcessingMode.BodySendMode
    request_trailer_mode: ProcessingMode.HeaderSendMode
    response_trailer_mode: ProcessingMode.HeaderSendMode
    def __init__(self, request_header_mode: _Optional[_Union[ProcessingMode.HeaderSendMode, str]] = ..., response_header_mode: _Optional[_Union[ProcessingMode.HeaderSendMode, str]] = ..., request_body_mode: _Optional[_Union[ProcessingMode.BodySendMode, str]] = ..., response_body_mode: _Optional[_Union[ProcessingMode.BodySendMode, str]] = ..., request_trailer_mode: _Optional[_Union[ProcessingMode.HeaderSendMode, str]] = ..., response_trailer_mode: _Optional[_Union[ProcessingMode.HeaderSendMode, str]] = ...) -> None: ...

class HttpStatus(_message.Message):
    __slots__ = ["code"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: StatusCode
    def __init__(self, code: _Optional[_Union[StatusCode, str]] = ...) -> None: ...
