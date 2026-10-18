
import subprocess 
from pathlib import Path 
import os
import json
from collections import defaultdict

current_dir = Path(__file__).parent


def _parse_rg_output(jsons):
    res = {}
    for i in jsons:
        data_type = i.get('type')
        text = ""
        if data_type == 'match':
            data = i.get('data')
            path = data["path"]

            if path.get('text'):
                path = path.get('text')
            else:
                path = path.get('bytes')
            
            res.setdefault(path,{'match':[],'hit':0,'lines':0})
            hit = len(data['submatches'])
            for j in data["submatches"]:
                line = data['line_number']
                text += f"{j["match"]["text"]} "
            res[path]['match'].append((line,text))
            res[path]['hit']+=hit
            res[path['lines']]+=1
    return res


def _char_mode(
        path,start,
        page,width,
        encoding,
        max_char
    ):
    num_chars = page*width

    content = ""
    info = []

    with open(path,mode="r",encoding=encoding,errors="replace") as f:
        f.read(start)
        body_text = f.read(num_chars)
        end_line = f.readline()

    if len(end_line)+num_chars>max_char+100:
        end_line = end_line[:100]
        info.append(
            ("info","超出预设范围，行补全仅展示100字符")
        )
    finished = len(body_text) < num_chars or end_line == ""
    info+=[
        ('next',
         num_chars+start+len(end_line) 
         if finished else "null"
         ),
        ('total_chars',num_chars+len(end_line)),
        ('completion_char',len(end_line))
    ]
    content+=body_text+end_line

    return content,info,finished


def _line_mode(
        path,start,
        page,width,
        encoding,
        max_char
    ):

    usage = 0
    content = ""
    info = []
    finished = False
    
    with open(path,mode="r",encoding=encoding,errors="replace") as f:
        temp = ""
        for i in range(start+page) :

            if i <start:
                temp = f.readline()
                continue

            line = f.readline()
            if line == "":
                finished = True
                break
            line=f"{i+1}:{line}"
            if len(line)+usage>max_char:
                info.append((
                    "warning",
                    f"第{i+1}行超出字符限制已暂停读取,建议用char 模式 start={len(temp+content) if len(temp+content) else 0}"
                ))
                break
            usage+=len(line)
            content+=line
    return content,info,finished



def read_file(
        path,start,
        unit,width,
        mode,encoding,
        max_char
        ):
    start-=1

    if start<1:
        start = 0
    
    if mode=="char":
        return _char_mode(path,start,unit[0],width,encoding,max_char)
        
    return _line_mode(path,start,unit[1],width,encoding,max_char)


def grep(pattern,path,include=None):
    args=[
        f"{current_dir}/ripgrep/rg",
        "--no-config",
        "--json",
        "-e",
        pattern,
    ]

    res = {}
    err = {}
    if include:
        args+=["-g",include]

    args+=["--",path]
    
    cmd_res = subprocess.run(
        args,
        capture_output=True
    )
    jsons = [json.loads(i) for i in cmd_res.stdout.splitlines()]
    
    if jsons:
        res = _parse_rg_output(jsons)

    if cmd_res.stderr.decode():  
        err = {'err':cmd_res.stderr.decode()}
    return res,err


if __name__ == "__main__":
    # print(grep("十","/home/xuanyansx/tmp/cg","text*"))
    a = grep("alpha", "/home/xuanyansx/Desktop/deepseek-agent/data/tmp/repro/perm")
    # a = grep("zzzz", "/home/xuanyansx/Desktop/deepseek-agent/data/tmp/repro/clean")    
    print(a)
