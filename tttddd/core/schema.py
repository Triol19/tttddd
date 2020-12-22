from typing import (  # noqa: I101
    Any,
    Dict,
    Generic,
    Optional,
    TypeVar,
    TypedDict,
)

from pydantic.generics import BaseModel, GenericModel
from pydantic_typeddict import parse_dict

__all__ = (
    'Error',
    'ErrorMessage',
    'SuccessResponseSchema',
    'EmptyResponseSchema',
    'ErrorResponseSchema',
)


class ErrorMessage(TypedDict):
    message: str
    type: str
    trace_id: Optional[str]
    details: Optional[Dict[str, Any]]


Error = parse_dict(ErrorMessage)


class EmptyResponseSchema(BaseModel):
    code: int


class ErrorResponseSchema(BaseModel):
    code: int
    error: Error  # type: ignore


T = TypeVar('T')


class SuccessResponseSchema(GenericModel, Generic[T]):
    code: int
    data: T
