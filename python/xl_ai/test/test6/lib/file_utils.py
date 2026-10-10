
import subprocess 
from pathlib import Path 
import os
import json

current_dir = Path(__file__).parent

def _func(n,code,f,byte,char):
    res = f.read(n-byte)
    return char+len(res.decode(code)),n


def _parse_rg_json(json_text,code):
    # ai生成，懒得写了,然后按我的需求改了下 2026/10/09 19:18
    results = []
    last_path = None
    f = None

    for line in json_text.splitlines():
        obj = json.loads(line)
        if obj["type"] != "match":
            continue
        data = obj["data"]
        path = data["path"]["text"]
        base = data["absolute_offset"]

        if last_path != path:
            if f:
                f.close()
            f = open(path,mode="rb")
            temp_byte = 0
            temp_char = 0
        
        for sub in data["submatches"]:
            d = {}
            byte_start = base + sub["start"]
            byte_end = base + sub["end"]
            char_start,temp_byte = _func(byte_start, code,f,temp_byte,temp_char)
            temp_char = char_start
            char_end,temp_byte = _func(byte_end, code,f,temp_byte,temp_char)
            temp_char = char_end

            d[sub["match"]["text"]] = {
                "path":path,
                "char_start":char_start,
                "char_end":char_end
            }
            results.append(d)
        last_path = path

    f.close()
    return results

def _char_mode(
        path,start,
        pages,width,
        encoding,
        max_char
    ):
    nlimit = width * pages
    r1_text = ""
    r2_text = ""
    if nlimit-start>max_char:
        nlimit = max_char
        r1_text = f"「内容超过2000，已被截断」"
    
    with open(path,mode="r",encoding=encoding) as f:
        f.read(start)
        text = f.read(nlimit)
        end_line = f.readline()

    if len(end_line):
        if (nlimit-start)+len(end_line)>=max_char+100:
            end_line = "<(超出范围，只展示部分)>\n"+end_line[
                :(max_char+100)-(nlimit-start)
            ]

        r2_text = f"↳ 「断行续接」（此内容仅作为下文的补充内容）：\n{end_line}"

    return f"""
从{start}字符位置出发，读{pages}页，宽度{width}字符
===============================================
{text}
===============================================
{r1_text}
{r2_text}
    """

def _line_mode(
        path,start,
        pages,width,
        encoding,
        max_char
    ):
    usage = 0

    with open(path,"r",encoding=encoding) as f:
        for i in range(start):
            f.readline()

        res = ""
        r_text = ""
        for i in range(pages):
            text = f.readline()
            if len(text)+usage>max_char:
                text=text[
                    :max_char-usage
                    ]
                r_text = f"已被截断，{pages-i}行没有被显示"
                break
            res+=text
            usage+=len(text)
    return f"""
从{start}行出发，读{pages}行
===============================================
{res}
===============================================
{r_text}

"""



def read_file(
        path,start,
        pages,width,
        mode,encoding,
        max_char
        ):
    
    if mode=="char":
        return _char_mode(path,start,pages,width,encoding,max_char)
    return _line_mode(path,start,pages,width,encoding,max_char)


def grep(pattern,path,include=None,encoding="utf-8"):
    args=[
        f"{current_dir}/ripgrep/rg",
        "--json",
        "--no-config",
        "-e",
        pattern,
    ]
    if include:
        args+=["-g",include]

    args+=["--",path]
    
    res = subprocess.run(
        args,
        capture_output=True
    )
    if res.returncode == 0:
        return _parse_rg_json(res.stdout.decode(),encoding)

    return {"stderr":res.stderr,"stdout":res.stdout,"returncode":res.returncode}



if __name__ == "__main__":
    # print(grep(
    #     "shorin",
    #     "/tmp/readme.txt"
    #     )
    # )
    print(
        read_file(
            "/home/xuanyansx/tmp/cg/text",
            0,2,1,"line","utf-8",2000
        )
    )
    




