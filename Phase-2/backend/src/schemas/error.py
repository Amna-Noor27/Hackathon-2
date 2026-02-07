from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):
    """
    Standardized error response format.
    """
    error: ErrorDetail


class ErrorDetail(BaseModel):
    """
    Details about the error.
    """
    type: str
    message: str
    detail: Optional[str] = None


# Example usage in API responses:
# {
#     "error": {
#         "type": "validation_error",
#         "message": "Invalid input data",
#         "detail": "Title field is required"
#     }
# }