import click

from flights import Flights


@click.command()
@click.option('--file', '-f', required=True, type=click.Path(exists=True), help='Path to the CSV file')
@click.option('--output', '-o', type=click.Path(writable=True), default=None,
              help='Path to the output csv file (optional)')
def process_flights(file: str, output: str):
    flights = Flights(file, ['flight ID', 'Arrival', 'Departure', 'success'])
    flights.load_flights()
    flights.check_success()
    # sort by arrival
    flights.flights = dict(sorted(flights.flights.items(), key=lambda item: item[1].arrival))
    csv_output = ''
    # print header to screen
    click.echo(','.join(flights.header))
    for f in flights.flights.values():
        # print flight
        click.echo(str(f))
        # add flight to csv file str
        if output:
            csv_output += f'{str(f)}\n'
    if output:
        # writes to csv
        flights.write_flights_to_csv(output)


if __name__ == '__main__':
    process_flights()
