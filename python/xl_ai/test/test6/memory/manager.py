from pathlib import Path
import json

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


# a = Archive()

# a.add_archive("114514")