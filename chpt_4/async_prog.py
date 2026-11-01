import asyncio
import time


# 1. Define the coroutine
async def fetch_data(task_id):
    print(f"Task {task_id}: Starting request...")
    
    # 2. Await the I/O operation. 
    # asyncio.sleep simulates waiting for a database or API response.
    await asyncio.sleep(2) 
    
    print(f"Task {task_id}: Done!")
    return f"Data {task_id}"

async def main():
    start_time = time.time()
    
    # 3. Schedule multiple coroutines to run concurrently
    results = await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3)
    )
    
    print(f"Finished in {time.time() - start_time:.2f} seconds")
    print(f"Results: {results}")

# 4. Start the event loop (this is the entry point)
if __name__ == "__main__":
    asyncio.run(main())