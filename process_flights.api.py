from typing import List

import click
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from flights import Flight, Flights

app = FastAPI()

# The db simulated in memory
flights = None


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"An internal server error occurred. Please try again later. error: {str(exc)}"}
    )


@app.get("/flights/{flight_id}", response_model=Flight)
async def get_flight_info(flight_id: str):
    global flights
    flight = flights.flights.get(flight_id)
    if flight:
        return flight
    else:
        raise HTTPException(status_code=404, detail="Flight not found")


@app.post("/flights/")
async def update_flights(flight_updates: List[Flight]):
    updated_flights = []
    print(flight_updates)
    for f in flight_updates:
        flights.flights[f.id] = f
        updated_flights.append(f.id)

        # Calculate successes after update
        flights.check_success()
        # Update the csv file
        await flights.write_flights_to_csv_async(flights.csv_file)

    return {"updatedFlights": updated_flights}


@click.command()
@click.option('--file', '-f', required=True, type=click.Path(exists=True), help='Path to the flight CSV file')
def run(file):
    # Load CSV file on startup
    @app.on_event("startup")
    async def startup_event():
        global flights
        flights = Flights(file, ['flight ID', 'Arrival', 'Departure', 'success'])
        await flights.load_flights_async()
        flights.check_success()

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == '__main__':
    run()
