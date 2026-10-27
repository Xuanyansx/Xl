
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
    
    with open(path,"r",encoding=encoding,errors='replace',newline="") as f:

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

                if l-len(line)-1!=0:
                    info+=[(
                        "warning",
                        f"第{i}行截断{'' if c==0 else f',本行还剩{l-len(line)-1}字符'}"
                    ),
                    (
                        'info',
                        f"start={i} {'' if c==0 else f' offset={c}'}可取到截断行后的内容"
                    )
                    ]
                jd = True

            usage+=len(line)
            content+=prefix+line

        if f.readline() == "":
            finished = False
            
    return content,info,finished



def base_read_file(path,start,lines,offset,encoding,max_char):
    info = []
    
    if start<1:
        info+=[
            ("warning",
            f"start:{start}非法，以替换为1")
        ]
        start = 1

    return _new_line(path,start,lines,offset,encoding,max_char,info)
    
     

def base_grep(max_columns,pattern,path,include=None,max_count=None):
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


def base_write_file(path,text,mode,encoding):
    with open(path,mode,encoding=encoding,newline="") as f:
        f.write(text)
    return 'Updated file'

def base_edit_file(path,old_string,new_string,replace,encoding):
    content = ''
    info = ''

    if old_string=='':
        raise ValueError(f"old_string为空")

    with open(path,'r',encoding=encoding,newline="") as f:
        file_text = f.read()
        i = file_text.find(old_string)
        
        if i==-1:
            return f'无匹配'
        
        if file_text.find(
            old_string,
            i+len(old_string)
            )>0 and not replace:
            return f'错误，存在多处匹配'

        if replace:
            content = file_text.replace(old_string,new_string)
            info = f'编辑成功,替换{file_text.count(old_string)}处'
        
        else:
            head = file_text[:i]
            tail = file_text[i+len(old_string):]
            content = head+new_string+tail
            info = f'编辑成功'


    with open(path,'w',encoding=encoding,newline="") as f:
        f.write(content)

    return info
                


if __name__ == "__main__":
    print("debug")
    # f = read_file("/tmp/rt/empty.txt",1,100,10,'utf-8',8000)
    # print(f)
    f1 = base_read_file("/home/xuanyansx/install.log",1,0,0,'utf-8',1000)
    print(f1)
    f2 = base_read_file("/home/xuanyansx/a.txt",5,1,4,'utf-8',2)
    print(f2)