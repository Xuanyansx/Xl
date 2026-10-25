
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




def _new_line(path,start,lines,offset,encoding,max_char,info):
    content = ''

    usage = 0

    finished = True
    jd = False

    i = 0
    
    with open(path,"r",encoding=encoding,errors='replace') as f:

        while True:
            i+=1
            if i<start:
                if f.readline() == "":
                    info.append(("warning", f"start:{start} 超出文件行数(共{i-1}行)"))
                    return content, info, False
                continue

            if i==lines+start and lines!=0 or jd:
                break

            line = f.readline()
            prefix = f"{i}:"    

            if line=="":
                break

            if i==start:
                line = line[offset:]

            if line == "" and i==start:
                info+=[
                    ("warning",
                    f"{start}行，offset:{offset}越界")
                ]
                continue


            
            if len(line)+usage>max_char:
                l = len(line)
                line = line[:max_char-usage]
                c = len(line) if i!=start else len(line)+offset

                info+=[(
                    "warning",
                    f"第{i}行截断,本行还剩{l-len(line)字符}"
                ),
                (
                    'info',
                    f"start={i} offset={c}可取到截断行后的内容"
                )
                ]
                jd = True

            usage+=len(line)
            content+=prefix+line

        if f.readline() == "":
            finished = False
            
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


def read_file2(path,start,lines,offset,encoding,max_char):
    info = []
    
    if start<1:
        info+=[
            ("warning",
            f"start:{start}非法，以替换为1")
        ]
        start = 1


    if lines<0:
        raise ValueError(f"lines:{lines} 值非法")



    return _new_line(path,start,lines,offset,encoding,max_char,info)
    

        



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
    f = read_file2("/tmp/rt/empty.txt",1,100,10,'utf-8',8000)
    print(f)
    f1 = read_file2("/home/xuanyansx/a.txt",2,1,2,'utf-8',2)
    print(f1)
    f2 = read_file2("/home/xuanyansx/a.txt",5,1,4,'utf-8',2)
    print(f2)