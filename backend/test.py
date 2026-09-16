students = [
    {"name": "张三", "score": 95},
    {"name": "李四", "score": 87},
    {"name": "王五", "score": 76},
    {"name": "赵六", "score": 92},
    {"name": "孙七", "score": 68},
    {"name": "周八", "score": 81},
    {"name": "吴九", "score": 74},
    {"name": "郑十", "score": 89},
    {"name": "冯十一", "score": 93},
    {"name": "陈十二", "score": 66},
    {"name": "褚十三", "score": 78},
    {"name": "卫十四", "score": 85},
    {"name": "蒋十五", "score": 72},
    {"name": "沈十六", "score": 90},
    {"name": "韩十七", "score": 63},
    {"name": "杨十八", "score": 88},
    {"name": "朱十九", "score": 77},
    {"name": "秦二十", "score": 94},
    {"name": "尤二一", "score": 69},
    {"name": "许二二", "score": 83},
    {"name": "何二三", "score": 71},
    {"name": "吕二四", "score": 96},
    {"name": "施二五", "score": 65},
    {"name": "张二六", "score": 79},
    {"name": "孔二七", "score": 91}
]

idx_docs = sorted(range(len(students)), key=lambda x:students[x]["score"], reverse=True)[:5]
print([students[i] for i in idx_docs])