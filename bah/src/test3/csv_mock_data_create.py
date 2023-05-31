"""
Description: Module generates a csv file and stores it in current directory

"""

import csv
import random

# List of sports
sports = ["Football", "Basketball", "Baseball", "Soccer", "Tennis", "Golf", "Swimming", "Volleyball", "Hockey", "Cricket"]

# List of Names
names = ["Sally", "Tim", "Joe", "Taylor", "Brandon", "Luke", "Chris", "Eric"]


data = [
    (random.choice(names), random.randint(100000, 999999), random.choice(sports), random.choice("ABCDE"), random.randint(1, 100))
    for _ in range(10000000)
]

# Generate CSV file
with open("data.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    
    # Write header row
    writer.writerow(["Name", "Code", "Sport", "Letter", "Number"])
   
    writer.writerows(data) 
