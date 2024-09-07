import aiofiles
import csv
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

MAX_FLIGHTS = 20
MIN_SUCCESS_MINUTES = 180


class Flight(BaseModel):
    id: str
    arrival: str
    departure: str
    success: Optional[str] = None

    def __str__(self):
        return f'{self.id},{self.arrival},{self.departure},{self.success}'

    def calculate_time_diff(self):
        arrival = datetime.strptime(self.arrival.strip(), '%H:%M')
        departure = datetime.strptime(self.departure.strip(), '%H:%M')
        return (departure - arrival).total_seconds() / 60


class Flights:
    def __init__(self, csv_file: str, header: List[str]):
        self.csv_file = csv_file
        self.flights = {}
        self.header = header

    async def load_flights_async(self):
        async with aiofiles.open(self.csv_file, mode='r') as file:
            content = await file.read()
            csv_reader = csv.DictReader(content.splitlines())

            for row in csv_reader:
                key = row['flight ID']
                self.flights[key] = Flight(id=row['flight ID'], arrival=row['Arrival'], departure=row['Departure'])

    def load_flights(self):
        with open('db.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                key = row['flight ID']
                self.flights[key] = Flight(id=row['flight ID'], arrival=row['Arrival'], departure=row['Departure'])

    def check_success(self):
        success_ids = []
        for f in self.flights:
            time = self.flights[f].calculate_time_diff()
            if time >= MIN_SUCCESS_MINUTES:
                success_ids.append(self.flights[f].id)
            else:
                self.flights[f].success = 'fail'
        success = 'success'
        if len(success_ids) > MAX_FLIGHTS:
            success = 'fail'
        for sid in success_ids:
            self.flights[sid].success = success

    async def write_flights_to_csv_async(self, output_file: str):
        async with aiofiles.open(output_file, mode='w') as file:
            await file.write(",".join(self.header) + "\n")

            for flight in self.flights.values():
                row = [
                    flight.id,
                    flight.arrival,
                    flight.departure,
                    flight.success or ''
                ]
                await file.write(",".join(row) + "\n")

    def write_flights_to_csv(self, output_file: str):
        with open(output_file, mode='w', newline='') as file:
            file.write(",".join(self.header) + "\n")
            for flight in self.flights.values():
                row = [
                    flight.id,
                    flight.arrival,
                    flight.departure,
                    flight.success or ''
                ]
                file.write(",".join(row) + "\n")
