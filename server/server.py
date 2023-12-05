import asyncio
import logging

from aiohttp import web
import aiofiles
import os
import config


async def archive(request):
    logging.info("Start archive")

    hash_ = request.match_info['archive_hash']
    direction = os.path.join(config.PHOTO_DIR, hash_)

    if not os.path.exists(direction):
        return web.HTTPNotFound(body="<h1>404 Not Found</h1><p>Архив не существует или был удален.</p>",
                                content_type="text/html")

    response = web.StreamResponse()
    response.headers['Content-Disposition'] = f'attachment; filename="photos_{hash_}.zip"'
    response.headers['Content-Type'] = 'application/zip'
    await response.prepare(request)

    commands = ['zip', '-r', '-', direction]
    pipe = asyncio.subprocess.PIPE
    proc = await asyncio.create_subprocess_exec(*commands, stdout=pipe, stderr=pipe, cwd=direction)
    try:
        while True:
            data = await proc.stdout.read(1024)
            if not data:
                await response.write_eof(data)
                break

            logging.info(f"Sending archive chunk {len(data)} bytes...")

            await response.write(data)
            if config.ENABLE_DELAY:
                await asyncio.sleep(1)

    except asyncio.CancelledError:
        logging.info(f"Download of {direction} was INTERRUPTED.")
        raise asyncio.CancelledError

    finally:
        if proc.returncode:
            proc.kill()
            await proc.communicate()
        return response


async def handle_index_page(request):
    async with aiofiles.open('html/index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


def create_app():
    app = web.Application()
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', archive),
    ])
    return app
