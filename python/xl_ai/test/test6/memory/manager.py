from typing import Annotated,Literal
from pathlib import Path
import json
import os
current_dir = Path(__file__).parent

class Archive:
    def __init__(self, dir=None):
        self.dir = Path(
            dir or current_dir
        ) / "archive"
        
        self.dir.mkdir(parents=True, exist_ok=True)
        self.meta_path = self.dir / "data.json"
        self._meta = json.loads(
            self.meta_path.read_text(
                encoding="utf-8"
            )
        )
        self.lid = self._meta["last_id"]

    def add_archive(self, msg) -> int:
        msg = "".join(msg)
        lid = self.lid
        (self.dir / f"{lid}.md").write_text(msg, encoding="utf-8")
        self.lid = lid + 1
        self._save_meta()
        return lid

    def get_archive(self, id) -> str:
        return (self.dir / f"{id}.md").read_text(encoding="utf-8")

    def _save_meta(self):
        self._meta["last_id"] = self.lid
        self.meta_path.write_text(
            json.dumps(self._meta, ensure_ascii=False),
            encoding="utf-8",
        )

class MemoryTool:
    def __init__(self):
        ...

    def get_memory_index(
            self,
            type:Literal["self","main","normal"]
            ):
        """
        获取type的记忆索引，
        通过索引调用指定的工具可以得到记忆。
        self：关于自己的记忆
        main：重要的记忆
        normal：普通的记忆
        """
        sL = ["self","main","normal"]
        if type not in sL:
            raise TypeError("参数类型不正确")
        
        return os.listdir(f"{current_dir}/{type}")

    def read_memory(self,memory_name,offset,limit):
        ...

    def read_memory_grep(self,memory_name,v):
        ...

    def edit_self_memory(self,memory_name,memory):
        ...

    def upsert_memory(self,memory_name,memory):
        ...





if __name__ == "__main__":
    print(os.listdir(f"{current_dir}/self"))
# a = Archive()

# a.add_archive("114514")