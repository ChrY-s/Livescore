from frontend.server import main as main_frontend
from backend.match_publishers.football.runner import main as main_backend
import asyncio

mains = []

async def main():
    mains.append(asyncio.create_task(main_frontend()))
    mains.append(asyncio.create_task(main_backend()))

    await asyncio.gather(*mains)

if __name__ == '__main__':
    asyncio.run(main())