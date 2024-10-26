import os
import json


def file(file_path, mode="r", new_data=None, json_=False) -> dict:
    try:
        with open(file_path, mode) as file:
            if mode == "r":
                if json_:
                    return json.load(file)
                else:
                    # print(file.read())
                    data = f"""[{file.read().strip(',').replace("'", '"')}]"""
                    return json.loads(data)
            
            elif mode == "a":
                if json_:
                    pass
                else:
                    file.write(f"{new_data},")
            elif mode == "w":
                if not json_:
                    data= str(new_data).strip('[]')+','
                    file.write(data)

    except Exception as e:
        print(f"Error at file(): {e}")

    return {}

def update_init(file_path, primary_key, new_data):
    if not os.path.isfile(file_path):
        with open(file_path, "w") as file:
            file.write("{}")
    with open(file_path, "r+") as file:
        data = json.load(file)
        data[primary_key] = new_data
        
        # Seek to the beginning of the file to overwrite the existing content
        file.seek(0)
        
        # Write the modified data back to the file
        json.dump(data, file) #, indent=4)



class DB:
    database_name = 'vinson.db'
    doc_names = file(f"{database_name}/init.json", json_=True) or ">> No Documents"    
    os.makedirs(database_name, exist_ok=True)
    # doc_names =[os.path.splitext(entry.name)[0] for entry in os.scandir('vinson.db') if entry.is_file()]

    def __init__(self, document_name = None):
        init_file = f"{DB.database_name}/init.json"
        self.document_name = document_name
    
        if document_name not in DB.doc_names:
            self.set_keys([])
            file(f"{DB.database_name}/{document_name}.txt", mode="w", new_data='', json_=False)
            print("created document: ", document_name)
        
        self.all_documents = file(init_file, json_=True)


    def set_keys(self, keys:list):
        update_init(file_path=f"{DB.database_name}/init.json", primary_key=self.document_name, new_data=keys)


    def add(self, data):
        if not self.all_documents[self.document_name]:
            self.set_keys(list(data.keys()))
            self.all_documents[self.document_name] =list(data.keys())
        if list(data.keys()) == self.all_documents[self.document_name]:
            file(f"{DB.database_name}/{self.document_name}.txt", mode="a", new_data = data, json_=False)
            return True
        else:
            raise Exception(f"Keys does not match, Please refer to document keys: {self.all_documents[self.document_name]}")
        

    def read_document(self) -> dict:
        return file(file_path=f"{DB.database_name}/{self.document_name}.txt")
    
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
            # self.save_document(document)
            file(file_path=f"{DB.database_name}/{self.document_name}.txt", mode="w", new_data=document)
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
            file(file_path=f"{DB.database_name}/{self.document_name}.txt", mode="w", new_data=document)
            # self.save_document(document)
            return f"Updated {len(matching_items)} items."
        
        return "No matching items found."


