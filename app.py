import sqlite3
from enum import Enum 

class Actions(Enum):
     ADD = 1
     DISPLAY_1 = 2
     DISPLAY_ALL = 3
     DEL_1 = 4
     DEL_ALL = 5
     UPDATE = 6
     EXIT = 7

def menu():
    for action in Actions:
        print(f'{action.name} - {action.value}')
    return int(input("Please select action: "))  # Convert input to integer

con = sqlite3.connect("cars.db")
cur = con.cursor()
try:
    cur.execute("CREATE TABLE IF NOT EXISTS cars(color TEXT, model INT, brand TEXT)")
except: 
    pass

def user_input():
    cColor =  input("Please insert car color: ")
    while True:
        cModel = input("Please input car model (must be an integer): ")
        if cModel.isdigit():  
            break
        else:
            print("Invalid input. Please input an integer for the car model.")
    cBrand = input("Please input car brand: ")

    cur.execute("""
                INSERT INTO cars VALUES
                (?, ?, ?)
                """, (cColor, cModel, cBrand))
    con.commit()  

def delete_row():
   display_all()
   selected_kill = int(input("Please select ROWID of car you would like to delete: "))
   cur.execute("delete from cars where ROWID = ?", (selected_kill,))
   con.commit()

def delete_all():
    cur.execute("delete from cars")
    con.commit()


def display_1():
    display_all()
    selected_display = int(input("Please select ROWID of car you want to display: "))
    car = cur.execute("SELECT * FROM cars WHERE ROWID = ?", (selected_display,)).fetchone()
    if car:
        print(f"ROWID: {selected_display}")
        print(f"Color: {car[0]}")
        print(f"Model: {car[1]}")
        print(f"Brand: {car[2]}")
    else:
        print("Car not found.")

def update_car():
    display_all()
    selected_upd = int(input("Please select the ROWID of the car you wish to update: "))
    new_color = input("New color: ")
    new_model = input("New model: ")
    new_brand = input("New brand: ")
    cur.execute(f"UPDATE cars SET color = ?, model = ?, brand = ? WHERE ROWID = ?",
                (new_color, new_model, new_brand, selected_upd))
    con.commit()

def display_all():
    cars = cur.execute("SELECT ROWID, * FROM cars")
    print("ROWID\tColor\tModel\tBrand")
    for car in cars.fetchall():
        print(f"{car[0]}\t{car[1]}\t{car[2]}\t{car[3]}")


if __name__ == '__main__':
    while True:
        try:
            user_choice = menu()
        except: print("input invalid")
        if user_choice == Actions.ADD.value:
            user_input()
        elif user_choice == Actions.DISPLAY_1.value:
            display_1()
        elif user_choice == Actions.DISPLAY_ALL.value:
            display_all()
        elif user_choice == Actions.DEL_1.value:
            delete_row()
        elif user_choice == Actions.DEL_ALL.value:
            delete_all()
        elif user_choice == Actions.UPDATE.value:
            update_car()
        elif user_choice == Actions.EXIT.value:
            break  # Exit the loop if the user chooses EXIT
