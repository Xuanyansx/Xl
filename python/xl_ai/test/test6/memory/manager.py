from pathlib import Path
import json

current_dir = Path(__file__).parent

class Archive:
    def __init__(
            self,
            ):
        
        with open(
            f"{current_dir}/archive/data.json",
            encoding="utf-8",
        ) as f:
            self.data = json.load(f)
        
        self.lid = self.data["last_id"]

    @staticmethod
    def get_archive(id):
        ...

    
    def add_archive(self,msg):
        with open(
            f"{current_dir}/archive/{self.lid}.md",
            encoding="utf-8",
            mode="w"
            ) as f:
            f.write(msg)
        
        self.data["last_id"]+=1
        with open(
            f"{current_dir}/archive/data.json",
            encoding="utf-8",
            mode="w"
            ) as f:
            json.dump(self.data,f)


# a = Archive()

# a.add_archive("114514")