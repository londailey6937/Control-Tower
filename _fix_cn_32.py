#!/usr/bin/env python3
"""Replace CN Section 3.2 Next Gate text in generate_guides.py."""

with open("generate_guides.py", "r") as f:
    content = f.read()

old_cn = (
    '    pdf.txt(\n'
    '        "\\u663e\\u793a\\u5c1a\\u672a\\u6279\\u51c6\\u7684'
    '\\u4e0b\\u4e00\\u4e2a\\u95e8\\u63a7\\u3002\\u683c\\u5f0f\\uff1a"\n'
    '        + LQ + "G1 (M+3)" + RQ + "\\u8868\\u793a\\u95e8'
    '\\u63a71\\u7684\\u76ee\\u6807\\u662f\\u7b2c3\\u4e2a\\u6708\\u3002"\n'
    '        "\\u8fd9\\u544a\\u8bc9PMP\\u4e0b\\u4e00\\u4e2a'
    '\\u51b3\\u7b56\\u68c0\\u67e5\\u70b9\\u5373\\u5c06\\u5230\\u6765\\u3002")'
)

new_cn = (
    '    pdf.txt(\n'
    '        "\\u663e\\u793a\\u4e0b\\u4e00\\u4e2a\\u5373\\u5c06'
    '\\u5230\\u6765\\u7684\\u51b3\\u7b56\\u95e8\\u63a7\\u3002"\n'
    '        "\\u5f53\\u95e8\\u63a7\\u72b6\\u6001\\u4e3a"'
    ' + LQ + "\\u5df2\\u6279\\u51c6" + RQ + "\\u3001"\n'
    '        "\\u51b3\\u7b56\\u4e3a"'
    ' + LQ + "\\u7ee7\\u7eed" + RQ + "\\u3001"\n'
    '        "\\u6216\\u6240\\u6709\\u51c6\\u5219\\u5fbd\\u7ae0'
    '\\u5747\\u6807\\u8bb0\\u4e3a\\u5b8c\\u6210\\u65f6\\uff0c"\n'
    '        "\\u8be5\\u95e8\\u63a7\\u89c6\\u4e3a\\u5df2\\u5b8c\\u6210\\u3002"\n'
    '        "\\u5f53\\u524d\\u95e8\\u63a7\\u7684\\u6240\\u6709\\u51c6\\u5219'
    '\\u6ee1\\u8db3\\u540e\\uff0c\\u6307\\u6807\\u4f1a\\u81ea\\u52a8\\u63a8\\u8fdb\\u3002"\n'
    '        "\\u683c\\u5f0f\\uff1a"'
    ' + LQ + "G1 (M+3)" + RQ +\n'
    '        "\\u8868\\u793a\\u95e8\\u63a71\\u7684\\u76ee\\u6807'
    '\\u662f\\u7b2c3\\u4e2a\\u6708\\u3002"\n'
    '        "\\u8fd9\\u544a\\u8bc9PMP\\u4e0b\\u4e00\\u4e2a'
    '\\u51b3\\u7b56\\u68c0\\u67e5\\u70b9\\u5373\\u5c06\\u5230\\u6765\\u3002")'
)

if old_cn in content:
    content = content.replace(old_cn, new_cn, 1)
    with open("generate_guides.py", "w") as f:
        f.write(content)
    print("SUCCESS: CN Section 3.2 updated")
else:
    print("ERROR: old CN text not found")
    # debug: print lines around 1202
    lines = content.split("\n")
    for i in range(1200, min(1210, len(lines))):
        print(f"  L{i+1}: {repr(lines[i])}")
