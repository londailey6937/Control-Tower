#!/usr/bin/env python3
"""Insert CN guide sections 15.3 and 25.2 for API removal docs."""

with open('generate_guides.py', 'r') as f:
    content = f.read()

# CN Section 15: Insert after the closing of section 15.2
cn15_end = r'\u4e2d\u56fd\u5927\u9646\u6295\u8d44\u8005\u5c24\u5176\u91cd\u8981\u3002")'
idx1 = content.find(cn15_end)
assert idx1 != -1, "CN section 15 end marker not found"
insert_pos1 = idx1 + len(cn15_end)

block1 = (
    '\n'
    '\n'
    '    pdf.sub("15.3 \\u79fb\\u9664\\u548c\\u6062\\u590dAPI\\u96c6\\u6210")\n'
    '    pdf.txt(\n'
    '        "PMP\\u3001\\u5546\\u4e1a\\u548c\\u6280\\u672f\\u89d2\\u8272\\u53ef\\u4ee5\\u79fb\\u9664\\u4e0d\\u9700\\u8981\\u7684API\\u96c6\\u6210\\u5361\\u7247\\u3002"\n'
    '        "\\u6bcf\\u5f20\\u5361\\u7247\\u53f3\\u4e0a\\u89d2\\u663e\\u793a\\u5173\\u95ed\\u6309\\u94ae(\\u2715)\\u3002\\u70b9\\u51fb\\u540e\\u663e\\u793a\\u786e\\u8ba4\\u63d0\\u793a\\uff0c"\n'
    '        "\\u786e\\u8ba4\\u540e\\u5361\\u7247\\u88ab\\u9690\\u85cf\\uff0c\\u64cd\\u4f5c\\u8bb0\\u5f55\\u5728\\u5ba1\\u8ba1\\u8ffd\\u8e2a\\u4e2d\\u3002\\n\\n"\n'
    '        "\\u5982\\u6709\\u96c6\\u6210\\u88ab\\u79fb\\u9664\\uff0c\\u9762\\u677f\\u5e95\\u90e8\\u4f1a\\u51fa\\u73b0\\u201c\\u6062\\u590d\\u5df2\\u79fb\\u9664\\u7684\\u96c6\\u6210\\u201d\\u6309\\u94ae\\uff0c"\n'
    '        "\\u70b9\\u51fb\\u53ef\\u6062\\u590d\\u6240\\u6709\\u9690\\u85cf\\u7684\\u5361\\u7247\\u3002\\u79fb\\u9664\\u72b6\\u6001\\u901a\\u8fc7localStorage\\u8de8\\u4f1a\\u8bdd\\u4fdd\\u7559\\u3002")\n'
)

content = content[:insert_pos1] + block1 + content[insert_pos1:]

# CN Section 25: Insert after SEC EDGAR kv
cn25_end = r'pdf.kv("SEC EDGAR", "\u76d1\u7ba1\u5907\u6848\u76d1\u63a7\u3001Form D\u8ffd\u8e2a\u3001\u6295\u8d44\u8005\u8d44\u8d28\u9a8c\u8bc1")'
idx2 = content.find(cn25_end)
assert idx2 != -1, "CN section 25 SEC EDGAR marker not found"
insert_pos2 = idx2 + len(cn25_end)

block2 = (
    '\n'
    '\n'
    '    pdf.sub("25.2 \\u79fb\\u9664\\u548c\\u6062\\u590dAPI\\u96c6\\u6210")\n'
    '    pdf.txt(\n'
    '        "PMP\\u3001\\u5546\\u4e1a\\u548c\\u6280\\u672f\\u89d2\\u8272\\u53ef\\u4ee5\\u70b9\\u51fb\\u5361\\u7247\\u4e0a\\u7684\\u5173\\u95ed\\u6309\\u94ae(\\u2715)\\u79fb\\u9664\\u4e0d\\u9700\\u8981\\u7684API\\u3002"\n'
    '        "\\u5df2\\u79fb\\u9664\\u7684\\u5361\\u7247\\u53ef\\u4ee5\\u968f\\u65f6\\u901a\\u8fc7\\u201c\\u6062\\u590d\\u5df2\\u79fb\\u9664\\u7684\\u96c6\\u6210\\u201d\\u6309\\u94ae\\u6062\\u590d\\u3002\\n\\n"\n'
    '        "\\u79fb\\u9664\\u64cd\\u4f5c\\u901a\\u8fc7localStorage\\u8de8\\u4f1a\\u8bdd\\u4fdd\\u7559\\uff0c\\u5e76\\u8bb0\\u5f55\\u5728\\u5ba1\\u8ba1\\u8ffd\\u8e2a\\u4e2d\\u3002")\n'
)

content = content[:insert_pos2] + block2 + content[insert_pos2:]

with open('generate_guides.py', 'w') as f:
    f.write(content)

print("OK - CN sections 15.3 and 25.2 inserted successfully")
