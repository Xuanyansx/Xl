
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
        limit,width,
        encoding,
        max_char
    ):
    num_chars = limit*width
    end_text = ""
    err_text = ""

    if num_chars>max_char:
        num_chars=max_char
        err_text = f"「内容超过{max_char}char，已被截断」"


    with open(path,mode="r",encoding=encoding,errors="replace") as f:
        f.read(start)
        body_text = f.read(num_chars)
        end_line = f.readline()


    if len(end_line):
        if num_chars+len(end_line)>=max_char+100:
            end_line = "(本行超出范围，只展示100char)\n"+end_line[
                :100
            ]
    end_text = f"↳ 「断行续接」（此内容是预览性质）：\n{end_line}"

    return f"""

从{start}字符位置出发，读{limit}页，宽度{width}字符
{'='*5}content{'='*5}
{body_text if body_text else "没有内容"}
{'='*5}断行续接{'='*5}
{end_text}
{'='*5}++++{'='*5}
{err_text}
本次读取了{len(body_text)}字符
当前在第{len(body_text)+start}字符（不包括断行续接）


"""


def _line_mode(
        path,start,
        limit,width,
        encoding,
        max_char
    ):
    usage = 0
    text = ""
    r_text = ""
    temp = ""

    line_pos = "末"
    with open(path,mode="r",encoding=encoding,errors="replace") as f:
        for i in range(start+limit) :
            is_end_text = "文件已读完"

            if i <start:
                temp = f.readline()
                continue
            line = f.readline()
            if line != "": 
                line_pos = i+1
                is_end_text = ""

            if len(line)>=max_char or len(line)+usage>=max_char:
                r_text = f"""
第{i+1}行超出字符限制已暂停读取
请用 char 模式 start={len(temp+text)-1 if len(temp+text) else 0} 读

计划读取{limit}行，还有{limit-(i-start)}行未读

"""
                break
            

                
            text+=line
            usage+=len(line)

    return f"""
从{start}行出发，读{limit}行
{'='*5}content{'='*5}
{text if text else "空"}
{'='*5}content{'='*5}
{is_end_text}
当前在第{line_pos}行
{r_text}
"""

def read_file(
        path,start,
        limit,width,
        mode,encoding,
        max_char
        ):
    
    if mode=="char":
        return _char_mode(path,start,limit,width,encoding,max_char)
        
    return _line_mode(path,start,limit,width,encoding,max_char)


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
    # print(
    #     read_file(
    #         "/home/xuanyansx/tmp/cg/text",
    #         2,1,1,"line","utf-8",2
    #     )
    # )

    # print(
    #     read_file(
    #         "/home/xuanyansx/tmp/cg/text",
    #         3,5,10,"char","utf-8",2
    #     )
    # )
    print(read_file("/tmp/t_big.log", start=0,width=10, limit=29, mode="line",encoding="utf-8",max_char=2000))

    print(
        read_file(
            "/tmp/huge_line.txt",
            0,3,80,"line","utf-8",2000
        )
    )




