# Vinson Database

Vinson Database is a lightweight, file-based Python database designed to manage structured data simply and efficiently. Optimized for handling CRUD operations with flexible querying and filtering capabilities, Vinson Database is ideal for small to medium datasets that require robust data manipulation without the overhead of traditional databases. The system also provides support for managing duplicates and indexing with primary keys.

## Features
- **Effortless Data Management**: Perform basic CRUD operations (Create, Read, Update, Delete) with ease.
- **Advanced Querying**: Retrieve data using primary keys, single-parameter queries, or multi-parameter queries for flexible data access.
- **Custom Updates**: Update records based on single or multiple fields with options for fast batch updates.
- **Duplicate Management**: Identify and remove duplicate records based on unique fields or entire records.

## Installation
To get started, clone the repository:
```bash
pip install vinson
```

## Usage Guide

### 1. Initialize the Database
Create a new database by instantiating the `DB` class with a database name:
```python
mydb = DB("studentsn")
```

### 2. Add Data
Add new data entries using the `add` method:
```python
mydb.add(data={"roll_no": i, "name": f"sonic{i}", "age": random.randint(10, 20)})
```

### 3. Read Data
Retrieve records with flexible querying options:
- **Primary Key Query**: Fetch a record by primary key:
    ```python
    mydb.primary_query(key='roll_no', value=11)
    ```
- **Single Parameter Query**: Retrieve records matching a single parameter:
    ```python
    mydb.query(key='name', value='sonic156')
    ```
- **Multiple Parameters Query**: Query data using multiple field-value pairs:
    ```python
    mydb.multiple_query(name='sonic1', age=15)
    ```

### 4. Update Data
Update specific records with both basic and fast update options:
```python
# Basic update based on a single parameter
mydb.update(criteria={'roll_no': 1}, updates={'name': 'sonicmc', 'age': 10})

# Fast update with multiple criteria
mydb.update_fast(criteria={'roll_no': 4, 'name': 'sonic4'}, updates={'age': 2})
```

### 5. Delete Data
Remove records based on specified criteria:
```python
mydb.delete_data(criteria={'name': 'sonic4', 'age': 2})
```

### 6. Handle Duplicates
Vinson Database provides methods to clean duplicate entries:
- **Remove duplicates based on a unique field** (e.g., `roll_no`):
    ```python
    mydb.delete_duplicates(unique_key='roll_no')
    ```
- **Remove duplicates based on the entire record**:
    ```python
    mydb.delete_duplicates()
    ```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

