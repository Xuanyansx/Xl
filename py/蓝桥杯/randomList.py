import random
rlist_len_max = 40
rlist_len_min = 10
item_max_size = 100

item_num = lambda :random.randint(rlist_len_min,rlist_len_max)
item = lambda :random.randint(0,item_max_size)
rlist = lambda :[item() for _ in range(item_num())]