"""

Streaming Process: Uses port 9999

Create a fake stream of data. 
Use temperature data from the batch process.

Reverse the order of the rows to read OLDEST data first.

Important! 

We'll stream forever - or until we read the end of the file. 
Use use Ctrl-C to stop. (Hit Control key and c key at the same time.)

Explore more at 
https://wiki.python.org/moin/UdpCommunication

"""
# Import from Python Standard Library

import csv
import socket
import time
import logging

# Set up basic configuration for logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Declare program constants (typically constants are named with ALL_CAPS)

HOST = "localhost"
PORT = 9999
ADDRESS_TUPLE = (HOST, PORT)
INPUT_FILE_NAME = "Life expectancy.csv"
OUTPUT_FILE_NAME = "out9.txt" 

# Define program functions (bits of reusable code)


import logging

def prepare_message_from_row(row):
    """Prepare a binary message from a given row."""
    Country, Year, Status, Life_expectancy, Adult_Mortality, Alcohol, percentage_expenditure, Hepatitis_B, BMI, Total_expenditure, HIV_AIDS, GDP, Population, Income_composition_of_resources, Schooling = row
    
    # Use an f-string to create a message from our data
    fstring_message = f"[{Country}, {Year}, {Status}, {Life_expectancy}, {Adult_Mortality}, {Alcohol}, {percentage_expenditure}, {Hepatitis_B}, {BMI}, {Total_expenditure}, {HIV_AIDS}, {GDP}, {Population}, {Income_composition_of_resources}, {Schooling}]"

    # Prepare a binary (1s and 0s) message to stream
    MESSAGE = fstring_message.encode()
    logging.debug(f"Prepared message: {fstring_message}")
    return MESSAGE



def stream_row(input_file_name, address_tuple):
    """Read from input file and stream data."""
    logging.info(f"Starting to stream data from {input_file_name} to {address_tuple}.")

    # Create a file object for input (r = read access)
    with open(input_file_name, "r") as input_file:
        logging.info(f"Opened for reading: {input_file_name}.")

        # Create a CSV reader object
        reader = csv.reader(input_file, delimiter=",")
        
        header = next(reader)  # Skip header row
        logging.info(f"Skipped header row: {header}")

        # use socket enumerated types to configure our socket object
        # Set our address family to (IPV4) for 'internet'
        # Set our socket type to UDP (datagram)
        ADDRESS_FAMILY = socket.AF_INET
        SOCKET_TYPE = socket.SOCK_DGRAM
        sock_object = socket.socket(ADDRESS_FAMILY, SOCKET_TYPE)

        rows = list(reader)
        last_processed_index = 0  # Track the index 

        with open(OUTPUT_FILE_NAME, "w") as output_file:
            logging.info(f"Opened for writing: {OUTPUT_FILE_NAME}.")
            while True: 
                for i in range(last_processed_index, len(rows)):
                    row = rows[i]
                    MESSAGE = prepare_message_from_row(row)
                    sock_object.sendto(MESSAGE, address_tuple)
                    output_file.write(str(MESSAGE) + "\n")
                    logging.info(f"Sent and wrote: {MESSAGE} on port {PORT}. Hit CTRL-c to stop.")

                last_processed_index = len(rows)  # Update the index 

                time.sleep(3)

# ---------------------------------------------------------------------------
# If this is the script we are running, then call some functions and execute code!
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        logging.info("===============================================")
        logging.info("Starting fake streaming process.")
        stream_row(INPUT_FILE_NAME, ADDRESS_TUPLE)
        logging.info("Streaming complete!")
        logging.info("===============================================")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
