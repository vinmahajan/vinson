from vinson import DB

# Initialize the database
mydb = DB("students")

# Add test data
mydb.add(data={"roll_no": 1, "name": "sonic1", "age": 19})
mydb.add(data={"roll_no": 2, "name": "sonic2", "age": 20})
mydb.add(data={"roll_no": 3, "name": "sonic3", "age": 15})
mydb.add(data={"roll_no": 4, "name": "sonic4", "age": 16})
mydb.add(data={"roll_no": 5, "name": "sonic5", "age": 19})

# Example queries
# Primary key query
result = mydb.primary_query(key='roll_no', value=3)
print("Primary Key Query Result:", result)

# Single parameter query
result = mydb.query(key='age', value=19)
print("Single Parameter Query Result:", result)

# Multiple parameters query
result = mydb.multiple_query(name='sonic5', age=19)
print("Multiple Parameters Query Result:", result)
