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
                    file.write('')

    except:
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
            file(f"{DB.database_name}/{document_name}.txt", mode="w", json_=False)
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

    
