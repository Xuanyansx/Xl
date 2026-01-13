<script setup lang="ts">



import { ref ,watch} from 'vue';


let todo_list = ref([])

let user_input = ref("")

function get_now(){

    const now_date = new Date();
    const now_time = 
            now_date.getFullYear().toString().slice(-2) + '/' +
            (now_date.getMonth() + 1).toString().padStart(2, '0') + '/' +
            now_date.getDate().toString().padStart(2, '0') + ' ' +
            now_date.getHours().toString().padStart(2, '0') + ':' +
            now_date.getMinutes().toString().padStart(2, '0');
    return now_time
}

function DEL(i: number){
    todo_list.value.splice(i,1)
}


function ADD(){
    if (user_input.value){


        let todo = {
            text:user_input.value,
            b:false,
            now:get_now(),
            end:""
        }
        todo_list.value.push(todo)
        user_input.value = ""
    }
}

function todo_done(i: { b: boolean; end: string; }){
    i.b=!i.b
    i.end = i.b?get_now():""
}

</script>

<template>
<div class="bg">
    <div class="todo">
        <div class="title">
            <h1>TODO</h1>
        </div>
        <hr>
        <div class="InputBox">
            <input class="InputBt" v-model="user_input" placeholder="写点什么吧..." />
            <span class="sub" @click="ADD()">Add</span>
        </div>
        <div class="TodoList" >
            <div v-for="i:{},index in todo_list">
                <div :class="[i.b?'itemB':'item']" @click="todo_done(i)">
                    <input type="checkbox" v-model="i.b" class="check">
                    <span class="text" >{{ i.text }}</span>
                    <div class="time">
                        <span class="start">开始：{{ i.now }}</span>
                        <span class="end">结束：{{ i.end }}</span>                    
                    </div>
                    <span class="del" @click="DEL(index)">DEL</span>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<style scoped>
.bg {
    background: linear-gradient(135deg, #01030f, #1b0044, #002a57);
    background-size: 400% 400%;
    animation: gradientFlow 15s ease infinite;
    height: 100vh;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    user-select: none;

}

@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.todo {
    width: 800px;
    height: 850px;
    background: rgba(15, 15, 35, 0.55);
    border-radius: 16px;
    backdrop-filter: blur(25px) saturate(180%);
    box-shadow:
        inset 0 0 20px rgba(255, 255, 255, 0.08),
        0 8px 30px rgba(0, 0, 0, 0.5);
    padding: 30px 40px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.title {
    color: #d6d8ff;
    display: flex;
    justify-content: center;
    letter-spacing: 3px;
}

hr {
    border: none;
    height: 1px;
    background: rgba(255,255,255,0.1);
    margin: 15px 0 25px 0;
}

.InputBox {
    display: flex;
    margin-bottom: 25px;
    gap: 10px;
}

.InputBt {
    flex: 6;
    height: 38px;
    padding: 0 10px;
    border-radius: 6px;
    outline: none;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.05);
    color: #e8eaff;
    font-size: 15px;
    transition: 0.3s;
}
.InputBt::placeholder {
    color: rgba(255,255,255,0.35);
}
.InputBt:focus {
    border-color: rgba(120,120,255,0.4);
    background: rgba(255,255,255,0.1);
}

.sub {
    flex: 1;
    height: 38px;
    border-radius: 6px;
    background: linear-gradient(90deg, #4a00e0, #8e2de2);
    color: #fff;
    text-align: center;
    line-height: 38px;
    font-weight: 600;
    cursor: pointer;
    transition: 0.3s;
}
.sub:hover {
    opacity: 0.85;
}

.TodoList {
    display: flex;
    flex-direction: column;
    color: #e8eaff;
    overflow-y: auto;
    
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none; /* IE/Edge */
}

.TodoList::-webkit-scrollbar {
    display: none; /* Chrome / Safari */
}


.item, .itemB {
    margin-top: 18px;
    padding: 10px 14px;
    display: flex;
    align-items: center;
    border-radius: 8px;
    background: rgba(255,255,255,0.03);
    transition: all 0.25s ease;
    border: 1px solid transparent;
    cursor: pointer;

}
.item:hover, .itemB:hover {
    border-color: rgba(255,255,255,0.1);
    transform: translateY(-3px);
    background: rgba(255,255,255,0.05);
}

.text {
    margin: 0 12px;
    flex: 1;
    font-size: 16px;
}

.itemB .text {
    font-style: italic;
    color: #666b85;
    text-decoration: line-through;
}

.time {
    flex: 2;
    font-size: 13px;
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.start {
    color: rgba(255,255,255,0.6);
}
.end {
    color: rgba(255,255,255,0.3);
}

.check {
    width: 18px;
    height: 18px;
    accent-color: #4a00e0;
    cursor: pointer;
}

.del {
    cursor: pointer;
    padding: 4px 8px;
    margin-left: 10px;
    background: rgba(255, 80, 80, 0.15);
    border-radius: 4px;
    font-size: 14px;
    transition: 0.3s;
}
.del:hover {
    background: rgba(255, 80, 80, 0.35);
}
</style>

/**
突然发现以前养成的js习惯（在末尾加上;）没了，鉴定为写python写的 25/10/15

*/