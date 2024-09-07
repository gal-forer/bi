## Notes:  
* I did the task on the weekend so, I assumed some stuff
* I made a script for part one and an API for part two
* I wasn't sure in the get part if it's one flight or all of them, so I did both
* I did an upsert end point for part two, it wasn't clear from the text, and it was a post request not a put

## How to run

* `pip install -r requirements.txt`

### Script
* `python process_flights_script.py -f input.csv -o output.csv`
#### params
* --file, -f : the input CSV file
* --output, -o : the output CSV file(optional)

### API
* `python process_flights_api.py --file db.csv`
#### params
* --file, -f : the CSV file to load and store flights on
#### request examples

* #### get flights: 
`curl --location 'http://127.0.0.1:8000/flights/'`  

* #### get flight by id: 
`curl --location 'http://127.0.0.1:8000/flights/A12'`  

* #### add or update flights: 
`curl --location 'http://127.0.0.1:8000/flights' \
--header 'Content-Type: application/json' \
--data '[
  {
    "id": "A133",
    "arrival": "13:00",
    "departure": "15:00",
    "success": "success"
  },
  {
    "id": "A14",
    "arrival": "12:00",
    "departure": "16:00"
  }
]'`

