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


@APP.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hello, from AWS ECS!</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            h1 {
                font-size: 3em;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            p {
                font-size: 1.2em;
                margin-bottom: 30px;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
            }
            .badge {
                background: rgba(255,255,255,0.2);
                padding: 10px 20px;
                border-radius: 25px;
                display: inline-block;
                margin: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 Hello from AWS ECS! 🎉</h1>
            <p>Your containerized FastAPI application is running successfully!</p>
            <div class="badge">🐳 Docker</div>
            <div class="badge">🚀 AWS ECS</div>
            <div class="badge">⚡ FastAPI</div>
            <div class="badge">🔄 GitHub Actions</div>
        </div>
    </body>
    </html>
    """


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