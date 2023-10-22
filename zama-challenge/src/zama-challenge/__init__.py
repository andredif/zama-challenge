from .models import Message

DEFAULT_RESPONSE = {
    404: {
        "description": "Not found"
    },
    422: {
        "description" : "Validation Error",
    },
    500: {
        "description": "Internal Error",
        "model": Message
    }
}