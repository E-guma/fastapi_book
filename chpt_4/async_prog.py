import asyncio
import time


# Simulate an asynchronous request.
async def fetch_data(task_id):
    print(f"Task {task_id}: Starting request...")
    
    # Simulated I/O latency (database or API call).
    await asyncio.sleep(2) 
    
    print(f"Task {task_id}: Done!")
    return f"Data {task_id}"

async def main():
    start_time = time.time()
    
    # Run the requests concurrently.
    results = await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3)
    )
    
    print(f"Finished in {time.time() - start_time:.2f} seconds")
    print(f"Results: {results}")

# Entry point.
if __name__ == "__main__":
    asyncio.run(main())