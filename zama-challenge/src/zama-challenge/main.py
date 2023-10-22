import argparse
import os
from fastapi import FastAPI

from .routers import router
from .exceptions import *

app = FastAPI()

app.include_router(router)

app.add_exception_handler(Exception, unknown_exception_handler)
app.add_exception_handler(GenericException, unicorn_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(AlreadyExistsException, already_exists_exception_handler)
app.add_exception_handler(AlreadyPerformedException, already_performed_exception_handler)


parser = argparse.ArgumentParser()
parser.add_argument(
    "-d",
    "--debug",
    action='store_true',
    default=False,
    help=(
        "Provide debug mode. "
        "Example --debug', default=False"
    )
)
parser.add_argument(
    "-host",
    "--host",
    default="0.0.0.0",
    help=(
        "Provide server host. "
        "Example --host=192.168.10.4', default='0.0.0.0'"
    )
)
parser.add_argument(
    "-p",
    "--port",
    default="8000",
    help=(
        "Provide server port. "
        "Example --port=5681', default='8000'"
    )
)


if __name__ == "__main__":
    import uvicorn
    options = parser.parse_args()

    uvicorn.run("zama_challenge.main:app", host=options.host, port=int(options.port),
                reload=options.debug, log_config=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logging.json'))