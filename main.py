import csv
import requests

URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"

def main():
    # Download NYTimes Covid Database
    data = fetch_data(URL)
    
    # Process CSV data
    reader = process_data(data)
    
    # Construct 14 day lists of new cases for each states
    new_cases = calculate_new_cases(reader)

    # Create a list to store selected states
    states = process_input(new_cases)
    
    # Print out 7-day averages for this week vs last week
    comparative_averages(new_cases, states)


def calculate_new_cases(reader):
    """
    Calculate the new COVID cases for each state over the last 14 days.

    Args:
        reader: A CSV DictReader object containing the COVID data.

    Returns:
        A dictionary with states as keys and a list of new cases as values.
    """

    previous_cases = {}
    new_cases = {}

    for row in reader:
        current_state = row["state"]        
        current_cases = int(row["cases"])
                    
        if current_state not in new_cases:
            new_cases[current_state] = []
            previous_cases[current_state] = current_cases
        else:
            new_cases[current_state].append(current_cases - previous_cases[current_state])
            previous_cases[current_state] = current_cases
            
            if len(new_cases[current_state]) > 14:
                new_cases[current_state].pop(0)

    return new_cases
    
def comparative_averages(new_cases, states):
    """
    Prints the seven-day average of new COVID-19 cases for selected states, comparing the last week to the previous week.

    Args:
        new_cases (dict): Dictionary with state names as keys and lists of daily new cases as values.
        states (list): List of states selected by the user.

    Returns:
        None
    """
    for state in states:
        last_week_average = seven_day_average(new_cases[state][-7:])
        penultimate_week_average = seven_day_average(new_cases[state][:7])
        
        if last_week_average > penultimate_week_average:
            increase = calculate_percentage_change(last_week_average, penultimate_week_average)
            print(f"{state} had a 7-day average of {round(last_week_average)} and an increase of {round(increase)}%.")
        elif last_week_average < penultimate_week_average:
            decrease = calculate_percentage_change(penultimate_week_average, last_week_average)
            print(f"{state} had a 7-day average of {round(last_week_average)} and a decrease of {round(decrease)}%.")
        else:
            print(f"{state} had a 7-day average of {round(last_week_average)}, same as last week.")

                    

def seven_day_average(l):    
    return sum(l) / 7



def calculate_percentage_change(new, old):
    try:
        return ((new - old) / old) * 100
    except ZeroDivisionError:
        print("An error occured calculating the percentage")
        return None
    


def fetch_data(URL):
    try:
        download = requests.get(URL)
        download.raise_for_status()
        decoded_content = download.content.decode("utf-8")
        return decoded_content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    return



def process_data(data):
    try:
        file = data.splitlines()
        reader = csv.DictReader(file)
        return reader
    except Exception as e:
        print(f"Error processing csv data: {e}")
        

def process_input(new_cases):
    states = []
    print("Choose one or more states to view average COVID cases.")
    print("Press enter when done.\n")

    while True:
        state = input("State: ")
        if state == "":
            break
        elif state in new_cases:
            states.append(state)
        else:
            print(f"Invalid state: {state}. Please enter a valid state name")


    print(f"\nSeven-Day Averages") if len(states) > 0 else print("No state selected")
    return states


    
main()

