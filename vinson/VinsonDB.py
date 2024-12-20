import os
import json


def file(file_path, mode="r", new_data=None, is_json=False):
    try:
        if mode == "r":
            with open(file_path, mode) as file:
                if is_json:
                    return json.load(file)
                else:
                    # Read and format non-JSON data as list of dicts/objects
                    data = f"""[{file.read().strip(',').replace("'", '"')}]"""
                    return json.loads(data)

        elif mode in {"a", "w"}:
            with open(file_path, mode) as file:
                if is_json:
                    json.dump(new_data, file)
                else:
                    # Append or write formatted data
                    # data_str = str(new_data).strip("[]") + ","
                    file.write(new_data)

    except Exception as e:
        print(f"Error in file(): {e}")

    return {}

def update_init(file_path, primary_key, new_data):
    # Ensure the file exists and contains a JSON object
    if not os.path.isfile(file_path):
        with open(file_path, "w") as file:
            json.dump({}, file)

    # Read, update, and save the JSON data
    with open(file_path, "r+") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}  # Initialize to empty if JSON is malformed

        # Update data with primary_key entry
        data[primary_key] = new_data
        
        # Write the updated JSON data back to the file
        file.seek(0)
        json.dump(data, file)
        file.truncate()  # Remove any remaining content if file was larger

    return f"Updated data for key: {primary_key}"



class DB:
    database_name = 'vinson.db'
    doc_names = file(f"{database_name}/init.json", is_json=True) or ">> No Documents"    
    os.makedirs(database_name, exist_ok=True)
    # doc_names =[os.path.splitext(entry.name)[0] for entry in os.scandir('vinson.db') if entry.is_file()]

    def __init__(self, document_name = None):
        init_file = f"{DB.database_name}/init.json"
        self.document_name = document_name
    
        if document_name not in DB.doc_names:
            self.set_keys([])
            # self.save_document('')
            file(f"{DB.database_name}/{document_name}.txt", mode="w", new_data='')
            print("created document: ", document_name)
        
        self.all_documents = file(init_file, is_json=True)


    def set_keys(self, keys:list):
        update_init(file_path=f"{DB.database_name}/init.json", primary_key=self.document_name, new_data=keys)


    def add(self, data):
        if not self.all_documents[self.document_name]:
            self.set_keys(list(data.keys()))
            self.all_documents[self.document_name] =list(data.keys())

        if list(data.keys()) == self.all_documents[self.document_name]:
            file(f"{DB.database_name}/{self.document_name}.txt", mode="a", new_data = f"{data},")
            return True
        else:
            raise Exception(f"Keys does not match, Please refer to document keys: {self.all_documents[self.document_name]}")
        

    def read_document(self) -> dict:
        return file(file_path=f"{DB.database_name}/{self.document_name}.txt")
    
    def save_document(self, document):
        data = str(document).strip('[]')+','
        file(file_path=f"{DB.database_name}/{self.document_name}.txt", mode="w", new_data=data)

    def get_key(self):
        return self.all_documents[self.document_name]
    
    def primary_query(self, key, value):
        document = self.read_document()
        data_dict = {item[key]: item for item in document}
        return data_dict.get(value, "Not found")
        
    def query(self, key, value):
        document = self.read_document()
        result = [item for item in document if item.get(key) == value]
        return result if result else "Not found"

    def multiple_query(self, **kwargs):
        document = self.read_document()
        # Filter the document based on all key-value pairs in kwargs
        result = [item for item in document if all(item.get(k) == v for k, v in kwargs.items())]
        return result if result else "Not found"

    def update(self, criteria, updates):
        document = self.read_document()

        # Flag to track if any item was updated
        updated = False
        
        # Update each item in the document if it matches all criteria
        for item in document:
            if all(item.get(k) == v for k, v in criteria.items()):
                # Apply all updates to the item
                for update_key, update_value in updates.items():
                    item[update_key] = update_value
                updated = True
        
        # Save the updated document back to storage if changes were made
        if updated:
            self.save_document(document)
            # file(file_path=f"{DB.database_name}/{self.document_name}.txt", mode="w", new_data=document)
        return "Update completed" if updated else "No matching items found"

    def update_fast(self, criteria, updates):
        document = self.read_document()  # Load the data

        # Use list comprehension to find items matching criteria
        matching_items = [item for item in document if all(item.get(k) == v for k, v in criteria.items())]
        
        # Apply updates only if there are matching items
        if matching_items:
            for item in matching_items:
                item.update(updates)  # Efficient update with dict.update()
            
            # Save only if there were updates
            self.save_document(document)  # Save the updated document
            # file(file_path=f"{DB.database_name}/{self.document_name}.txt", mode="w", new_data=document)
            return f"Updated {len(matching_items)} items."
        
        return "No matching items found."

    def delete_data(self, criteria):
        document = self.read_document()  # Load the data
        initial_length = len(document)
        
        # Filter out items that match the criteria
        document = [item for item in document if not all(item.get(k) == v for k, v in criteria.items())]
        
        # Check if any items were removed
        if len(document) < initial_length:
            self.save_document(document)  # Save the updated document
            return f"Deleted {initial_length - len(document)} items."
        
        return "No matching items found."


    def delete_duplicates(self, unique_key=None):
        document = self.read_document()  # Load the data
        seen = set()
        unique_data = []

        # Loop through each item in the document
        for item in document:
            # Define what makes the item unique (based on unique_key or entire item)
            identifier = item[unique_key] if unique_key else frozenset(item.items())
            
            # Add only the first occurrence of each unique identifier
            if identifier not in seen:
                seen.add(identifier)
                unique_data.append(item)
        
        # Save the cleaned document back to storage if duplicates were removed
        if len(unique_data) < len(document):
            self.save_document(unique_data)
            return f"Removed {len(document) - len(unique_data)} duplicates."

        return "No duplicates found."
