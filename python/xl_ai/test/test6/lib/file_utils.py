
import subprocess 
from pathlib import Path 
import os
import json
from collections import defaultdict

current_dir = Path(__file__).parent


def _parse_rg_output(jsons,max_columns):

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
            
            res.setdefault(path,{'match':[],'lines':0})
            hit = len(data['submatches'])
            line = data['line_number']
            text = data['lines']['text']

            if len(text)>max_columns:
                text = f"[Omitted long line with {hit} matches]"
            res[path]['match'].append((line,text))
            res[path]['lines']+=1
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
        next_line = f.readline()

    if len(end_line)+num_chars>max_char+100:
        end_line = end_line[:100]
        info.append(
            ("info","超出预设范围，行补全仅展示100字符")
        )
    finished = len(body_text) < num_chars or next_line == ""
    info+=[
        ('next',
         num_chars+start+len(end_line)+1
         if not finished else "null"
         ),
        ('本次读取字符数',len(body_text+end_line)),
        ('行补全字数',len(end_line))
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
        temp = 0
        for i in range(start+page) :

            if i <start:
                temp = len(f.readline())
                continue

            line = f.readline()
            if line == "":
                finished = True
                break
            line=f"{i+1}:{line}"
            if len(line)+usage>max_char:
                content+=line[:max_char-usage]

                info.append((
                    "warning",
                    f"第{i+1}行超出字符限制已暂停读取,建议用char 模式 start={temp+len(content) if temp+len(content) else 0}"
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


def grep(max_columns,pattern,path,include=None,max_count=None):
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
    
    if max_count:
        args+=["-m",max_count]

    args+=["--",path]
    
    cmd_res = subprocess.run(
        args,
        capture_output=True
    )
    jsons = [json.loads(i) for i in cmd_res.stdout.splitlines()]
    
    if jsons:
        res = _parse_rg_output(jsons,max_columns)

    if cmd_res.stderr.decode():  
        err = {'err':cmd_res.stderr.decode()}
    return res,err


if __name__ == "__main__":
    print("debug")
    f = read_file("/home/xuanyansx/a.txt",500,(2,2),80,"char","utf-8",2000)
