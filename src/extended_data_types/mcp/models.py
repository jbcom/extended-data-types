"""Pydantic models for MCP server responses."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ParameterInfo(BaseModel):
    """Information about a function parameter.

    Attributes:
        name: Parameter name.
        type_hint: Type annotation as string.
        default: Optional default value.
        description: Parameter description from docstring.
    """

    name: str = Field(..., description="Parameter name")
    type_hint: str = Field(..., description="Type annotation as string")
    default: str | None = Field(None, description="Optional default value")
    description: str = Field(..., description="Parameter description from docstring")


class FunctionInfo(BaseModel):
    """Basic function information for listing and search.

    Attributes:
        name: Function name.
        module: Module path where function is defined.
        category: Functional category (e.g., 'serialization', 'file_operations').
        signature: Full function signature as string.
        return_type: Return type annotation as string.
        description: Short description from docstring.
        parameters: List of parameter information.
        related_functions: List of related function names.
    """

    name: str = Field(..., description="Function name")
    module: str = Field(..., description="Module path where function is defined")
    category: str = Field(
        ...,
        description="Functional category (e.g., 'serialization', 'file_operations')",
    )
    signature: str = Field(..., description="Full function signature as string")
    return_type: str = Field(..., description="Return type annotation as string")
    description: str = Field(..., description="Short description from docstring")
    parameters: list[ParameterInfo] = Field(
        default_factory=list, description="List of parameter information"
    )
    related_functions: list[str] = Field(
        default_factory=list, description="List of related function names"
    )


class SearchResult(BaseModel):
    """Search result with relevance scoring.

    Attributes:
        function_id: Unique identifier for the function.
        name: Function name.
        category: Functional category.
        description: Short description.
        score: Relevance score (0-1).
        signature: Function signature.
    """

    function_id: str = Field(..., description="Unique identifier for the function")
    name: str = Field(..., description="Function name")
    category: str = Field(..., description="Functional category")
    description: str = Field(..., description="Short description")
    score: float = Field(..., ge=0.0, le=1.0, description="Relevance score (0-1)")
    signature: str = Field(..., description="Function signature")


class Documentation(BaseModel):
    """Complete function documentation.

    Attributes:
        function_id: Unique identifier for the function.
        name: Function name.
        module: Module path.
        category: Functional category.
        signature: Function signature.
        return_type: Return type annotation.
        description: Short description.
        long_description: Extended description from docstring.
        parameters: List of parameter information.
        returns: Description of return value.
        raises: List of exceptions that can be raised.
        examples: List of usage examples.
        related_functions: List of related function names.
    """

    function_id: str = Field(..., description="Unique identifier for the function")
    name: str = Field(..., description="Function name")
    module: str = Field(..., description="Module path")
    category: str = Field(..., description="Functional category")
    signature: str = Field(..., description="Function signature")
    return_type: str = Field(..., description="Return type annotation")
    description: str = Field(..., description="Short description")
    long_description: str = Field(
        ..., description="Extended description from docstring"
    )
    parameters: list[ParameterInfo] = Field(
        default_factory=list, description="List of parameter information"
    )
    returns: str = Field(..., description="Description of return value")
    raises: list[str] = Field(
        default_factory=list, description="List of exceptions that can be raised"
    )
    examples: list[str] = Field(
        default_factory=list, description="List of usage examples"
    )
    related_functions: list[str] = Field(
        default_factory=list, description="List of related function names"
    )
