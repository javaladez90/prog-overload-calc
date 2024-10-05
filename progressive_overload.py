import datetime
import math

# Set up basic data storage
#List to store workout data

workout_data = []

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
    
#fucntion to view workout data
def view_workout_data():
    if not workout_data:
        print("No workout data available. \n")
        return 
    
    print("Workout Data:")
    for session in workout_data:
        print(f"Date: {session['data']}, Exercise: {session['exercise']}, Weight: {session['weight']} lbs, Reps: {session['reps']}")
    print("\n")
    
#function to suggest the next weight for progressive overload
def suggest_next_weight(exercise_name, target_reps, increment=2.5):
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
        print("4. Quit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            add_workout_data()
        elif choice == '2':
            view_workout_data()
        elif choice == '3':
            exercise_name = input("Enter the exercise name to get the next weight suggestion: ").lower().replace(" ", "_")
            target_reps = int(input("Enter the target number of reps: "))
            suggest_next_weight(exercise_name, target_reps)
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break;
        else: 
            print("Invalid choice, try again.\n")
            
# Run the program
if __name__ == "__main__":
    main()