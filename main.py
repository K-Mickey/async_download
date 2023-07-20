from aiohttp import web

from server.arg_parse import run_parser
from server.logger import set_logs
from server.server import create_app

if __name__ == '__main__':
    run_parser()
    set_logs()
    app = create_app()
    web.run_app(app)
