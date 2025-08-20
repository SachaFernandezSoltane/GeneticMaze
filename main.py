import asyncio
from src.maze.maze_app import MazeApp

app = MazeApp(7, 11, 10, 100)  # rows, cols, population, refresh timer en ms

async def main_loop():
    await app.run_async()

asyncio.run(main_loop())
