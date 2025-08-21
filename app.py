import argparse
import logging
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        try:
            logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)
        except Exception:
            logging.exception("Issue initializing logs")

        self.default_name = "World"


APP = App()


@APP.get("/")
async def root():
    return "{ \"unavailable\" }"


@APP.get("/hello/{name}")
async def hello(name: str) -> str:
    return f"Hello {name}!"


@APP.get("/healthcheck")
async def healthcheck() -> str:
    return "OK"


def parse_args(args):
    argparser = argparse.ArgumentParser(description="Development server")
    argparser.add_argument("-p", "--port", type=int, default=7101, help="Port for HTTP server (default=%d)." % 7101)
    argparser.add_argument("-l", "--log-level", default="debug", help="Log level.")
    return argparser.parse_args(args)


def main(args=None):
    args = parse_args(sys.argv[1:] if args is None else args)
    port = args.port or 7101
    logging.info("Starting server on port %s with log level=%s", args.port, args.log_level)
    uvicorn.run("app:APP", host="0.0.0.0", port=port, log_level=args.log_level, reload=True)


if __name__ == "__main__":
    main()