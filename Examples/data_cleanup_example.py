from vinson import DB

# Initialize the database
mydb = DB("students")

# Add sample duplicate data
sample_data = [
    {"roll_no": 1, "name": "sonic1", "age": 19},
    {"roll_no": 2, "name": "sonic2", "age": 18},
    {"roll_no": 1, "name": "sonic1", "age": 19},  # Duplicate entry
    {"roll_no": 3, "name": "sonic3", "age": 17},
]

# Adding sample data to the database
for data in sample_data:
    mydb.add(data=data)

# Display before removing duplicates
print("Before Removing Duplicates:", mydb.read_all())

# Remove duplicates based on a unique field (roll_no)
mydb.delete_duplicates(unique_key='roll_no')

# Display after removing duplicates by roll_no
print("After Removing Duplicates by roll_no:", mydb.read_all())

# Add another duplicate entry for full record cleanup demonstration
mydb.add(data={"roll_no": 2, "name": "sonic2", "age": 18})  # Duplicate entry

# Remove duplicates based on the entire record
mydb.delete_duplicates()

# Display after removing duplicates based on entire record
print("After Removing Duplicates by entire record:", mydb.read_all())
