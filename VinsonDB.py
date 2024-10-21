import os
import json
# import ast

class DB:

    def __init__(self):
        # self.db_name = db_name
        self.dbpath = 'vinson.db'
        os.makedirs(self.dbpath, exist_ok=True)
        self.document_names = {os.path.splitext(entry.name)[0]:{} for entry in os.scandir(self.dbpath) if entry.is_file()}
        try:
            with open(f"{self.dbpath}/init.txt", "r") as file:
                data = file.read()
        except:
            pass
    

    def create_document(self, document_name):
        path =f"{self.dbpath}/{document_name}.txt"
       
        if document_name not in self.document_names:
            with open(path, 'w') as file:
                file.write('')
        
            print("created document: ", document_name)
            self.document_names.append(document_name)
            return True
        else:
            print("document already exist.")
            return False


    def add(self, document_name, data):
        if document_name in self.document_names:
            with open(f"{self.dbpath}/{document_name}.txt", "a") as file:
                file.write(f"{data},")
            # print("data added sucessfully.", data)
            return True
        else:
            raise Exception("Document does not exist")
            # return False

    def read_document(self, document_name):
        with open(f"{self.dbpath}/{document_name}.txt", "r") as file:
            data = f"""[{file.read().strip(',').replace("'", '"')}]"""
            return json.loads(data)
    
    def get_key(self, document_name):
        with open(f"{self.dbpath}/{document_name}.txt", "r") as file:
            data = file.read()
        return list(data[0].keys())

    def query(self,document_name):
        return self.read_document(document_name)

    def printname(self):
        print(self.dbpath)
        print(self.document_names)