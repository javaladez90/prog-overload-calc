import datetime
import math
import json
import os

# Set up basic data storage
#List to store workout data

workout_data = []
print("Program started")
def load_workout_data():
    global workout_data
    print("Loading workout data...")
    print(f"Current working directory: {os.getcwd()}")
    if os.path.exists('workout_data.json'):
        with open('workout_data.json', 'r') as file:
            try:
                workout_data = json.load(file)
                print("Workout data loaded successfully!\n")
                print(f"Loaded data: {workout_data}\n") #debug statement to verify loaded data
            except json.JSONDecodeError:
                print("Error loading workout data. Starting with an empty list.\n")
                workout_data = []
    else:
        print("No existing workout data found. Starting fresh.\n")
        
#Function to save workout data to JSON file
def save_workout_data():
    with open('workout_data.json', 'w') as file:
        json.dump(workout_data, file, indent=4)
    print("Workout data saved successfully!\n")
    
    
# function to add new workout session data
def add_workout_data():
    #ask user for workout details
    date_input = input("Enter the date (YYYY-MM-DD) or type 't' for today's date: ")
    if date_input.lower() == 't':
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    elif '-' not in date_input:
        date = f"{date_input[:4]}-{date_input[4:6]}-{date_input[6:]}"
    else:
        date = date_input
        
    #Corrext time zone
    date = datetime.datetime.now().strftime("%Y-%m-%d") if date == datetime.datetime.now().strftime("%Y-%m-%d") else date
        
    exercise = input("Enter the exercise: ").lower().replace(" ","_")
    weight = float(input("Enter the weight lifted (lbs): "))
    reps = int(input("Enter the number of reps: "))
    
    #Create a dictionary 
    session = {
        "date": date,
        "exercise": exercise,
        "weight": weight,
        "reps": reps
    }
    
    #Append the workout session to the workout_data_list
    workout_data.append(session)
    print("Workout data added successfully!\n")
    
    save_workout_data()
#fucntion to view workout data
def view_workout_data():
    if not workout_data:
        print("No workout data available. \n")
        return 
    
    print("Workout Data:")
    for index,session in enumerate(workout_data):
        print(f"{index + 1}. Date: {session['date']}, Exercise: {session['exercise']}, Weight: {session['weight']} lbs, Reps: {session['reps']}")
    print("\n")
    
def delete_workout_data():
    if not workout_data:
        print("No workout data available to delete.\n")
        return
    
    view_workout_data()
    try:
        entry_number = int(input("Enter the number of the workout you want to delete: "))
        if 1 <= entry_number <= len(workout_data):
            deleted_session = workout_data.pop(entry_number - 1)
            print(f"Deleted workout: Date: {deleted_session['date']}, Exercise: {deleted_session['exercise']}, Weight: {deleted_session['weight']} lbs, Reps: {deleted_session['reps']}\n")
            #Save the workout
            save_workout_data()
        else:
            print("Invalid entry number. \n")
    except ValueError:
        print("Invalid input. Please enter a number. \n")
        

    
#function to suggest the next weight for progressive overload
def suggest_next_weight(exercise_name, target_reps):
    #filter out data for the selected exercise
    exercise_data = [d for d in workout_data if d["exercise"] == exercise_name]
    
    if not exercise_data:
        print(f"No data available for the exercise '{exercise_name}'. Please provide your initial weight.")
        return None
    
    # sort data by date
    exercise_data.sort(key=lambda x: x['date'])
    
    #get the most recent data
    latest_record = exercise_data[-1]
    weight = latest_record["weight"]
    reps = latest_record["reps"]
    
    #calculate the next weight suggestion using a formula based on reps and weight 
    one_rep_max = weight * (1 + reps / 30)
    #Adjust weight increment based on target reps
    if target_reps > 1:
        next_weight = one_rep_max / (1 + target_reps / 30)
    else:
        next_weight = one_rep_max
    next_weight = round(next_weight, 2) # Round to 2 decimal places
    

    
    print(f"Based on your last session of {weight} lbs for {reps} reps, the suggested for {target_reps} reps is {next_weight} lbs. \n")
 

    #Recommend 1rm, 3rm, and 5rm
    
    three_rep_max = round(one_rep_max / (1 + 3 / 30), 2)
    five_rep_max = round(one_rep_max / (1 + 5 / 30), 2)
    
    print(f"Estimated 1 Rep Max: {round(one_rep_max, 2)} lbs")
    print(f"Estimated 3 Rep Max: {three_rep_max} lbs")
    print(f"Estimated 5 Rep Max: {five_rep_max} lbs\n")
    
    return next_weight

#Menu to interact with the program
def main():
    while True:
        print("What would you like to do?")
        print("1. Add workout data")
        print("2. View workout data")
        print("3. Suggest next weight for progressive overload")
        print("4. Delete workout data")
        print("5. Quit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            add_workout_data()
        elif choice == '2':
            view_workout_data()
        elif choice == '3':
            exercise_name = input("Enter the exercise name to get the next weight suggestion: ").lower().replace(" ", "_")
            target_reps = int(input("Enter the target number of reps: "))
            suggest_next_weight(exercise_name, target_reps)
        elif choice == '4':
            delete_workout_data()
        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break;
        else: 
            print("Invalid choice, try again.\n")
            
# Run the program
if __name__ == "__main__":
    main()