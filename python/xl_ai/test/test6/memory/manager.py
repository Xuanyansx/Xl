from typing import Annotated,Literal
from pathlib import Path
import json
import os
import lib.file_utils as fu
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
            mtype:Literal["self","main","normal"],
            enable_advanced:Annotated[bool,"启用高级搜索模式，默认false"]=False,
            pattern:Annotated[str,"高级模式，ripgrep风格的正则，默认为None"]=None,
            glob:Annotated[str,"高级模式，glob表达式，搜索某类型下符合条件的记忆，默认none"]=None
        ):
        """
        获取type的记忆索引，
        通过索引调用指定的工具可以得到记忆的名称。
        self：关于自己的记忆
        main：重要的记忆
        normal：普通的记忆

        默认enable_advanced=false即为不启用高级匹配，
        未启用高级模式下会输出mtype下所有的记忆
        
        启用后会grep的模式扫描mtype类型下符合pattern和glob的记忆
        """
        sL = ["self","main","normal"]
        content = ""
        if mtype not in sL:
            raise TypeError("参数类型不正确")
        
        if enable_advanced:
            if glob and not pattern:
                raise ValueError("glob不可以单独使用")
            
            res,err = fu.base_grep(
                1,
                pattern,
                f'{current_dir}/{mtype}',
                glob
            )


            if res:
                paths = list(res.keys())

                for path in paths:
                    content+=f"{path.rsplit("/")[-1]},"
            if err:
                content += f"<error>\n{err['err']}</error>"

            return content

        return f"{mtype}:{os.listdir(f'{current_dir}/{mtype}')}"

    def read_memory(
            self,
            memory_name:Annotated[str,"记忆名称"],
            mtype:Literal["self","main","normal"],
            start_line:Annotated[int,"起始行号默认为1"]=1,
            lines: Annotated[int,"从start行开始读取的行数，默认为0；0表示读到文件末尾"]=0,
            skip_chars:Annotated[int,"start_line行内过的字符数，默认0"]=0,
            max_char:Annotated[int,"最大输出字符数量，最大为32000默认为8000"]=8000
        ):
        """
        通过记忆类型mtype和记忆名称memory_name获取记忆内容
        操作模式和返回类型类似read_file
    
        """



        info_text = ""
        
        content,info,finished = fu.base_read_file(
            f'{current_dir}/{mtype}/{memory_name}',
            start_line,
            lines,
            skip_chars,
            "utf-8",
            max_char
        )

        for name,text in info:
            info_text+=f"# {name}:{text}\n"

        return f"""
<content>
{content}
</content>
# next_line:{finished}
{info_text}
"""        

    def read_memory_grep(
            self,
            mtype,
            pattern:Annotated[str,"ripgrep风格的正则"],
            glob:Annotated[str,"glob表达式，搜索某类型下符合条件的记忆"]=None,
            max_count:Annotated[str,"每个文件最大输出行数，默认None"]=None
        ):
        """
        扫描匹配符合要求的记忆
        返回内容与行号
        
        """
        MAX_COLUMNS = 100
        res,err = fu.base_grep(MAX_COLUMNS,pattern,f'{current_dir}/{mtype}',glob,max_count)
        content = ""

        #直接就是拷贝 2026/10/28 21:10:

        if res:
            keys = list(res.keys())

            for i in keys:
                content+=f"[{i}]\n<content>\n"
                lines = res[i]['lines']
                for line,text in res[i]['match']:
                    content+=f"{line}:{text}\n"
                content+=f"</content>\n#lines:{lines}\n\n"

        if err:
            content += f"<error>\n{err['err']}</error>"
        return content

    def edit_self_memory(
            self,
            mtype:Literal["self","main","normal"],
            memory_name:Annotated[str,"记忆名称"],
            old_string:Annotated[str,'字面文本,精确匹配'],
            new_string:Annotated[str,'替换文本,空字符串即删除该段'],
            replace:Annotated[bool,'布尔,默认 false;true 则替换全部匹配']=False,
        ):
        """
        编辑一个文件，将old_string替换为new_string
        
        """

        res = fu.base_edit_file(
            f'{current_dir}/{mtype}/{memory_name}',
            old_string,
            new_string,
            replace,
            'utf-8'
        )
        return res  

    def write_memory(
            self,
            mtype:Literal["self","main","normal"],
            memory_name:Annotated[str,"记忆名称"],
            mode:Literal["w","a"],
            memory
        ):

        """
        创建或者写入一个记忆文件
        mode为w，当文件存在时清空内容写入，文件不存创建并写入
        mode为a时为追加模式，在文件末尾追加内容
        """

        res = fu.base_write_file(
        f'{current_dir}/{mtype}/{memory_name}',
            memory,
            mode,
            'utf-8'
        )
        return res




if __name__ == "__main__":
    print(os.listdir(f"{current_dir}/self"))
# a = Archive()

# a.add_archive("114514")