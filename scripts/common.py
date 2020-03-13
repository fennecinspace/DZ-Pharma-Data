import json

class Json:
    @classmethod
    def save(cls, file_path, data):
        try:
            with open(file_path, 'w') as f:
                f.write(json.dumps(data))
                return True
        except Exception as e:
            print("Could not save to JSON file !")


    @classmethod
    def read(cls, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.loads(f.read())
        except Exception as e:
            print("Could not read from JSON file !")
            return {}