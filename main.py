import asyncio
import logging
from argparse import ArgumentParser
from aiopath import AsyncPath
from aioshutil import copyfile

parser = ArgumentParser()
parser.add_argument('source_path', type=str, help="Path to source folder")
parser.add_argument('dest_path', type=str, help="Destination path, where files will be copied")
args = parser.parse_args()

source_path = AsyncPath(args.source_path)
destination_path = AsyncPath(args.dest_path)

# # For Test
# source_path = AsyncPath('.')
# destination_path = AsyncPath('./copiedFiles')

logging.basicConfig(format='%(asctime)s %(message)s',
                    level=logging.ERROR,
                    handlers=[logging.FileHandler("app.log"),
                              logging.StreamHandler()])


async def main():
    files = await read_folder(source_path)
    coros = [copy_file(destination_path, file) async for file in files]
    return await asyncio.gather(*coros)

async def read_folder(path: AsyncPath):
    return path.rglob("*.*")

async def copy_file(dest_path: AsyncPath, file_path: AsyncPath):
    try:
        if file_path.suffix:
            full_dest_path = dest_path / file_path.suffix / file_path.name
        else:
            full_dest_path = dest_path / file_path.name / file_path.name

        await full_dest_path.parent.mkdir(parents=True, exist_ok=True)
        if full_dest_path != file_path:
            await copyfile(file_path, full_dest_path)

    except IsADirectoryError as e:
        logging.error(f"IsADirectoryError: {e}")
    except FileNotFoundError as e:
        logging.error(f"FileNotFoundError: {e}")
    except:
        logging.error("Unknown error in copy_file() function")

if __name__ == '__main__':
    asyncio.run(main())
