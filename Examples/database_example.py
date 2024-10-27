import random
from vinson import DB  # Assuming your main code is saved in vinson_database.py

# Initialize the database
mydb = DB("students")

# Add sample data
for i in range(1, 101):  # Adding 100 entries for demonstration
    mydb.add(data={"roll_no": i, "name": f"sonic{i}", "age": random.randint(10, 20)})

# Read Data
# Query by primary key
print("Primary Query:", mydb.primary_query(key='roll_no', value=11))

# Query by single parameter
print("Single Parameter Query:", mydb.query(key='name', value='sonic20'))

# Query by multiple parameters
print("Multiple Parameters Query:", mydb.multiple_query(name='sonic5', age=15))

# Update Data
# Update single record
mydb.update(criteria={'roll_no': 1}, updates={'name': 'sonic_updated', 'age': 21})

# Fast update with multiple criteria
mydb.update_fast(criteria={'roll_no': 4, 'name': 'sonic4'}, updates={'age': 22})

# Delete Data
# Delete by criteria
mydb.delete_data(criteria={'name': 'sonic10', 'age': 18})

# Handle Duplicates
# Remove duplicates by unique field
mydb.delete_duplicates(unique_key='roll_no')

# Remove duplicates based on entire record
mydb.delete_duplicates()

print("Database operations completed successfully.")
