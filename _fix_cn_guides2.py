#!/usr/bin/env python3
"""One-time script to update CN sections in generate_guides.py"""
import sys

with open('generate_guides.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# --- 1. Reorder CN tab kv lines ---
start = None
for i, line in enumerate(lines):
    if '\\u53cc\\u8f68\\u89c6\\u56fe' in line and '\\u6280\\u672f+' in line and i > 1000:
        start = i
        break

if start is None:
    print("ERROR: Could not find CN kv start line", file=sys.stderr)
    sys.exit(1)

kv_lines = lines[start:start+14]
print(f"Found CN kv block at line {start+1}")

# Old: 双轨0 门控1 风险2 时间线3 法规4 资金5 行动6 预算7 资源8 供应商9 审计10 美国11 文档12 留言板13
# New: 双轨 门控 法规 风险 审计 文档 行动 时间线 预算 资金 美国 资源 供应商 留言板
new_order = [0, 1, 4, 2, 10, 12, 6, 3, 7, 5, 11, 8, 9, 13]
reordered = [kv_lines[i] for i in new_order]

# Update audit trail description
for j, line in enumerate(reordered):
    if '\\u5ba1\\u8ba1\\u8ffd\\u8e2a' in line and '\\u6240\\u6709' in line:
        reordered[j] = line.replace(
            '\\u6240\\u6709\\u4eea\\u8868\\u76d8\\u64cd\\u4f5c\\u7684\\u65f6\\u95f4\\u5e8f\\u65e5\\u5fd7',
            '\\u670d\\u52a1\\u5668\\u7aef\\u6301\\u4e45\\u5316\\u7684\\u6240\\u6709\\u4eea\\u8868\\u76d8\\u64cd\\u4f5c\\u65f6\\u95f4\\u5e8f\\u65e5\\u5fd7'
        )

# Update MB description
for j, line in enumerate(reordered):
    if '\\u7559\\u8a00\\u677f' in line and 'PMP' in line:
        reordered[j] = '    pdf.kv("\\u7559\\u8a00\\u677f", "\\u76ee\\u6807\\u9a71\\u52a8\\u7684\\u7ed3\\u6784\\u5316\\u7ebf\\u7a0b\\u6d88\\u606f\\u3001\\u51b3\\u7b56\\u8bb0\\u5f55\\u3001\\u5de5\\u4f5c\\u6d41\\u7b5b\\u9009\\u548c\\u8d23\\u4efb\\u5236")\n'

lines[start:start+14] = reordered
print("1/2 CN tab order reordered")

# --- 2. Add CN section 5.3 ---
insert_after = None
for i, line in enumerate(lines):
    if 'business' in line and 'EM' in line and '\\u5546\\u4e1a' in line and i > 1000:
        insert_after = i
        break

if insert_after is None:
    print("ERROR: Could not find CN sec 5.2 end", file=sys.stderr)
    sys.exit(1)

print(f"Found CN sec 5.2 end at line {insert_after+1}")

sec53_lines = [
    '\n',
    '    pdf.sub("5.3 \\u91cc\\u7a0b\\u7891\\u8be6\\u60c5\\u5f39\\u7a97")\n',
    '    pdf.txt(\n',
    '        "\\u70b9\\u51fb\\u4efb\\u4f55\\u91cc\\u7a0b\\u7891\\u5361\\u7247\\u4f1a\\u6253\\u5f00\\u8be6\\u60c5\\u5f39\\u7a97\\uff0c\\u663e\\u793a\\u8def\\u5f84\\uff08\\u6280\\u672f\\u6216\\u6cd5\\u89c4\\uff09\\u3001"\n',
    '        "\\u76ee\\u6807\\u6708\\u4efd\\u3001\\u5f53\\u524d\\u72b6\\u6001\\uff0c\\u4ee5\\u53ca\\u91cc\\u7a0b\\u7891\\u8303\\u56f4\\u548c\\u8981\\u6c42\\u7684\\u8be6\\u7ec6\\u63cf\\u8ff0\\u3002\\n\\n"\n',
    '        "\\u8981\\u5173\\u95ed\\u5f39\\u7a97\\uff0c\\u70b9\\u51fb\\u5f39\\u7a97\\u5916\\u90e8\\u4efb\\u4f55\\u4f4d\\u7f6e\\uff08\\u53d8\\u6697\\u7684\\u906e\\u7f69\\u5c42\\uff09\\u5373\\u53ef\\u3002"\n',
    '        "\\u6ca1\\u6709\\u5173\\u95ed\\u6309\\u94ae\\uff0c\\u906e\\u7f69\\u5c42\\u70b9\\u51fb\\u6a21\\u5f0f\\u4fdd\\u6301\\u754c\\u9762\\u7b80\\u6d01\\u4e00\\u81f4\\u3002")\n',
]

# Find blank line after the closing paren
for i in range(insert_after, min(insert_after + 5, len(lines))):
    if lines[i].strip() == '':
        insert_pos = i + 1
        break
else:
    insert_pos = insert_after + 2

lines[insert_pos:insert_pos] = sec53_lines
print("2/2 CN section 5.3 added")

with open('generate_guides.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Done - generate_guides.py updated")
