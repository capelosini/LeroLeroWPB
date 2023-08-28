import base64
import json
import os

class Model:
    def __init__(self, modelFileName="model"):
        self.modelFileName=modelFileName
        if os.path.isfile(modelFileName):
            with open(modelFileName, "r") as f:
                self.model = json.loads(base64.b64decode(f.read().encode()).decode())
        else:
            self.model={"vocab": 0, "data": {}}
            self.save()

    def save(self):
        with open(self.modelFileName, "w") as f:
            f.write(base64.b64encode(json.dumps(self.model).encode()).decode())