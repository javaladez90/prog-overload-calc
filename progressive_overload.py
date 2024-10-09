import datetime
import math
import json
import os
import sqlite3
import matplotlib.pyplot as plt

# Set up basic data storage
#List to store workout data

workout_data = []

def connect_db():
    return sqlite3.connect('workout_data.db')

def initialize_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            exercise TEXT NOT NULL,
            weight REAL NOT NULL,
            reps INTEGER NOT NULL
        )
        ''')
    conn.commit()
    conn.close()

    
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
    
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO workouts (date, exercise, weight, reps)
        VALUES (?, ?, ?, ?)
        ''', (date,exercise, weight, reps))
    conn.commit()
    conn.close()
    print("Workout data added successfully!\n")
    
    

#fucntion to view workout data
def view_workout_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workouts')
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print("No workout data available.\n")
        return
    
    print("Workout Data:")
    for row in rows:
        print(f"ID: {row[0]}. Date: {row[1]}, Exercise: {row[2]}, Weight: {row[3]} lbs, Reps: {row[4]}")
    print("\n")
    
def delete_workout_data():
   view_workout_data()
   try:
        entry_id = int(input("Enter the ID of the workout you want to delete: "))
   
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM workouts WHERE id = ?', (entry_id,))
        conn.commit()
        conn.close()
        print("Workout deleted successfully!\n")
   except ValueError:
       print("Invalid input. Please enter a valid workout ID.\n")
   except sqlite3.Error as e:
       print(f"Database error: {e} \n")
    

    
#function to suggest the next weight for progressive overload
def suggest_next_weight(exercise_name, target_reps):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workouts WHERE exercise = ? ORDER BY date', (exercise_name,))
    exercise_data = cursor.fetchall()
    conn.close()
 
    if not exercise_data:
        print(f"No data available for the exercise '{exercise_name}'. Please provide your initial weight.")
        return None
    
    #calculate total volume and average weight for progressive overload
    total_weight = sum(record[3] * record[4] for record in exercise_data)
    total_reps = sum(record[4] for record in exercise_data)
    avg_weight = total_weight / total_reps
    
    #suggest the next weight average weight as baseline
    one_rep_max = avg_weight * (1 + (total_reps / len(exercise_data)) / 30)
    if target_reps > 1:
        next_weight = one_rep_max / (1 + target_reps / 30)
    else:
        next_weight = one_rep_max
    next_weight = round(next_weight, 2)
    
    print(f"Based on all your previous sessions, the suggested weight for {target_reps} reps is {next_weight} lbs. \n")
    
    #
    
    
   

    #Recommend 1rm, 3rm, and 5rm
    
    three_rep_max = round(one_rep_max / (1 + 3 / 30), 2)
    five_rep_max = round(one_rep_max / (1 + 5 / 30), 2)
    
    print(f"Estimated 1 Rep Max: {round(one_rep_max, 2)} lbs")
    print(f"Estimated 3 Rep Max: {three_rep_max} lbs")
    print(f"Estimated 5 Rep Max: {five_rep_max} lbs\n")
    
    return next_weight

def plot_workout_data():
    conn = connect_db()
    cursor = conn.cursor()
    exercise_name = input("Enter the exercise name to plot: ").lower().replace(" ", "_")
    cursor.execute('SELECT date, weight, reps FROM workouts WHERE exercise = ? ORDER BY date', (exercise_name,))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print("No workout data available for the selected exercise.\n")
        return
    
    #Extract data 
    dates = [datetime.datetime.strptime(row[0], "%Y-%m-%d") for row in rows]
    weights = [row[1] for row in rows]
    progressive_overload = []
    
    #Calculate progressive overload bsed on all previous session
    total_weight = 0
    total_reps = 0
    for row in rows:
        total_weight += row[1] * row[2]
        total_reps += row[2]
        avg_weight = total_weight / total_reps
        one_rep_max = avg_weight * (1 + (total_reps / len(rows)) / 30)
        progressive_overload.append(round(one_rep_max, 2))
    
    #Plot the data 
    plt.figure(figsize=(10, 5))
    plt.plot(dates, weights, marker='o', linestyle='-', color='b', label='Actual Weight Lifted')
    plt.plot(dates, progressive_overload, marker='x', linestyle='--', color='r', label='Suggested Progressive Overload')
    plt.xlabel('Date')
    plt.ylabel('Weight Lifted (lbs)')
    plt.title('Progression Over Time with suggested Progressive Overload')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.savefig('workout_progress.png')
    print("Plot saved as 'workout_progress.png.")

#Menu to interact with the program
def main():
    initialize_db()
    
    while True:
        print("What would you like to do?")
        print("1. Add workout data")
        print("2. View workout data")
        print("3. Suggest next weight for progressive overload")
        print("4. Delete workout data")
        print("5. Plot Workout data")
        print("6. Quit")
        
        choice = input("Enter your choice (1-6): ")
        
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
            plot_workout_data()
        elif choice == '6':
            print("Exiting the program. Goodbye!")
            break;
        else: 
            print("Invalid choice, try again.\n")
            
# Run the program
if __name__ == "__main__":
    main()