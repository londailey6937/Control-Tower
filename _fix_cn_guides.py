#!/usr/bin/env python3
"""One-time script to update CN sections in generate_guides.py"""
import sys

with open('generate_guides.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# --- 1. Reorder CN tab kv lines (1431-1444) ---
# Find the block by looking for the first CN kv line
start = None
for i, line in enumerate(lines):
    if '\\u53cc\\u8f68\\u89c6\\u56fe' in line and '\\u6280\\u672f+' in line and i > 1000:
        start = i
        break

if start is None:
    print("ERROR: Could not find CN kv start line", file=sys.stderr)
    sys.exit(1)

# Extract the 14 kv lines
kv_lines = lines[start:start+14]
print(f"Found CN kv block at line {start+1}")

# Build reordered lines - mapping old positions to new order
# Old order: 双轨(0), 门控(1), 风险(2), 时间线(3), 法规(4), 资金(5), 行动(6), 预算(7), 资源(8), 供应商(9), 审计(10), 美国(11), 文档(12), 留言板(13)
# New order: 双轨, 门控, 法规, 风险, 审计, 文档, 行动, 时间线, 预算, 资金, 美国, 资源, 供应商, 留言板
new_order = [0, 1, 4, 2, 10, 12, 6, 3, 7, 5, 11, 8, 9, 13]
reordered = [kv_lines[i] for i in new_order]

# Update audit trail description to mention server persistence
for j, line in enumerate(reordered):
    if '\\u5ba1\\u8ba1\\u8ffd\\u8e2a' in line and '\\u6240\\u6709' in line:
        reordered[j] = line.replace(
            '\\u6240\\u6709\\u4eea\\u8868\\u76d8\\u64cd\\u4f5c\\u7684\\u65f6\\u95f4\\u5e8f\\u65e5\\u5fd7',
            '\\u670d\\u52a1\\u5668\\u7aef\\u6301\\u4e45\\u5316\\u7684\\u6240\\u6709\\u4eea\\u8868\\u76d8\\u64cd\\u4f5c\\u65f6\\u95f4\\u5e8f\\u65e5\\u5fd7'
        )

# Update Message Board description
for j, line in enumerate(reordered):
    if '\\u7559\\u8a00\\u677f' in line and 'PMP' in line:
        reordered[j] = '    pdf.kv("\\u7559\\u8a00\\u677f", "\\u76ee\\u6807\\u9a71\\u52a8\\u7684\\u7ed3\\u6784\\u5316\\u7ebf\\u7a0b\\u6d88\\u606f\\u3001\\u51b3\\u7b56\\u8bb0\\u5f55\\u3001\\u5de5\\u4f5c\\u6d41\\u7b5b\\u9009\\u548c\\u8d23\\u4efb\\u5236")\n'

lines[start:start+14] = reordered
print("1/2 CN tab order reordered")

# --- 2. Add CN section 5.3 (milestone detail modal) ---
# Find the line with "business" + EM + CN text before section 6
insert_after = None
for i, line in enumerate(lines):
    if 'business' in line and 'EM' in line and '\\u5546\\u4e1a' in line and i > 1000:
        insert_after = i
        # Check next lines for "# 6"
        for j in range(i+1, min(i+5, len(lines))):
            if lines[j].strip() == '# 6':
                insert_after = i
                break
        break

if insert_after is None:
    print("ERROR: Could not find CN sec 5.2 end", file=sys.stderr)
    sys.exit(1)

print(f"Found CN sec 5.2 end at line {insert_after+1}")

# Insert section 5.3 after the closing paren of 5.2
sec53_lines = [
    '\n',
    '    pdf.sub("5.3 \\u91cc\\u7a0b\\u7891\\u8be6\\u60c5\\u5f39\\u7a97")\n',
    '    pdf.txt(\n',
    '        "\\u70b9\\u51fb\\u4efb\\u4f55\\u91cc\\u7a0b\\u7891\\u5361\\u7247\\u4f1a\\u6253\\u5f00\\u8be6\\u60c5\\u5f39\\u7a97\\uff0c\\u663e\\u793a\\u8def\\u5f84\\uff08\\u6280\\u672f\\u6216\\u6cd5\\u89c4\\uff09\\u3001"\n',
    '        "\\u76ee\\u6807\\u6708\\u4efd\\u3001\\u5f53\\u524d\\u72b6\\u6001\\uff0c\\u4ee5\\u53ca\\u91cc\\u7a0b\\u7891\\u8303\\u56f4\\u548c\\u8981\\u6c42\\u7684\\u8be6\\u7ec6\\u63cf\\u8ff0\\u3002\\n\\n"\n',
    '        "\\u8981\\u5173\\u95ed\\u5f39\\u7a97\\uff0c\\u70b9\\u51fb\\u5f39\\u7a97\\u5916\\u90e8\\u4efb\\u4f55\\u4f4d\\u7f6e\\uff08\\u53d8\\u6697\\u7684\\u906e\\u7f69\\u5c42\\uff09\\u5373\\u53ef\\u3002"\n',
    '        "\\u6ca1\\u6709\\u5173\\u95ed\\u6309\\u94ae\\uff0c\\u906e\\u7f69\\u5c42\\u70b9\\u51fb\\u6a21\\u5f0f\\u4fdd\\u6301\\u754c\\u9762\\u7b80\\u6d01\\u4e00\\u81f4\\u3002")\n',
]

# Find the blank line after the closing paren
insert_pos = insert_after + 1
while insert_pos < len(lines) and lines[insert_pos].strip() == ')' or lines[insert_pos].strip().endswith(')'):
    insert_pos += 1

# Insert before the blank line that precedes "# 6"
for i in range(insert_after, min(insert_after + 5, len(lines))):
    if lines[i].strip() == '':
        insert_pos = i + 1
        break

lines[insert_pos:insert_pos] = sec53_lines
print("2/2 CN section 5.3 added")

with open('generate_guides.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Done - generate_guides.py updated")
    content = f.read()

# 1. Fix CN tab order
old_cn_kv = (
    '    pdf.kv("\u53cc\u8f68\u89c6\u56fe", "\u6280\u672f+\u6cd5\u89c4\u91cc\u7a0b\u7891\u5e76\u6392\u663e\u793a")\n'
    '    pdf.kv("\u95e8\u63a7\u7cfb\u7edf", "\u5e26PMP\u6743\u9650\u63a7\u5236\u7684\u51b3\u7b56\u68c0\u67e5\u70b9")\n'
    '    pdf.kv("\u98ce\u9669\u4eea\u8868\u76d8", "ISO 14971\u98ce\u9669\u767b\u8bb0\u8868\uff0c\u5e26\u7b5b\u9009\u548c\u524d5\u6392\u540d")\n'
    '    pdf.kv("\u65f6\u95f4\u7ebf", "\u6280\u672f\u91cc\u7a0b\u7891\u7684\u5546\u4e1a\u8bed\u8a00\u7ffb\u8bd1")\n'
    '    pdf.kv("\u6cd5\u89c4\u8ffd\u8e2a", "IEC/ISO/21 CFR\u5408\u89c4\u6807\u51c6\u77e9\u9635")\n'
    '    pdf.kv("\u8d44\u91d1/\u8dd1\u9053", "\u8d22\u52a1\u72b6\u51b5\u3001\u71c3\u70e7\u7387\u3001\u878d\u8d44\u91cc\u7a0b\u7891\u548cAPI\u96c6\u6210")\n'
    '    pdf.kv("\u884c\u52a8\u9879", "\u4efb\u52a1\u770b\u677f\u3001DHF\u6587\u6863\u8ffd\u8e2a\u548cCAPA\u65e5\u5fd7")\n'
    '    pdf.kv("\u9884\u7b97", "\u6309\u7c7b\u522b\u7684\u9884\u7b97\u4e0e\u5b9e\u9645\u652f\u51fa")\n'
    '    pdf.kv("\u8d44\u6e90", "\u56e2\u961f\u5206\u914d\u548c\u4ea7\u80fd\u5229\u7528")\n'
    '    pdf.kv("\u4f9b\u5e94\u5546", "\u786c\u4ef6\u7ec4\u4ef6\u4f9b\u5e94\u5546\u8ffd\u8e2a")\n'
    '    pdf.kv("\u5ba1\u8ba1\u8ffd\u8e2a", "\u6240\u6709\u4eea\u8868\u76d8\u64cd\u4f5c\u7684\u65f6\u95f4\u5e8f\u65e5\u5fd7")\n'
    '    pdf.kv("\u7f8e\u56fd\u6295\u8d44", "\u5317\u7f8e\u878d\u8d44\u7ba1\u9053\u3001\u6295\u8d44\u8005\u8ffd\u8e2a\u548cIR\u6d3b\u52a8")\n'
    '    pdf.kv("\u6587\u6863\u63a7\u5236", "ISO 13485\u5bf9\u9f50\u7684\u6587\u6863\u751f\u547d\u5468\u671f\u3001\u4fee\u8ba2\u5386\u53f2\u548c\u5ba1\u67e5\u8ba1\u5212")\n'
    '    pdf.kv("\u7559\u8a00\u677f", "PMP\u4e0e\u5229\u76ca\u76f8\u5173\u65b9\u4e4b\u95f4\u7684\u53cc\u5411\u7ebf\u7a0b\u5f0f\u6280\u672f\u5bf9\u8bdd\u6d88\u606f")'
)

new_cn_kv = (
    '    pdf.kv("\u53cc\u8f68\u89c6\u56fe", "\u6280\u672f+\u6cd5\u89c4\u91cc\u7a0b\u7891\u5e76\u6392\u663e\u793a")\n'
    '    pdf.kv("\u95e8\u63a7\u7cfb\u7edf", "\u5e26PMP\u6743\u9650\u63a7\u5236\u7684\u51b3\u7b56\u68c0\u67e5\u70b9")\n'
    '    pdf.kv("\u6cd5\u89c4\u8ffd\u8e2a", "IEC/ISO/21 CFR\u5408\u89c4\u6807\u51c6\u77e9\u9635")\n'
    '    pdf.kv("\u98ce\u9669\u4eea\u8868\u76d8", "ISO 14971\u98ce\u9669\u767b\u8bb0\u8868\uff0c\u5e26\u7b5b\u9009\u548c\u524d5\u6392\u540d")\n'
    '    pdf.kv("\u5ba1\u8ba1\u8ffd\u8e2a", "\u670d\u52a1\u5668\u7aef\u6301\u4e45\u5316\u7684\u6240\u6709\u4eea\u8868\u76d8\u64cd\u4f5c\u65f6\u95f4\u5e8f\u65e5\u5fd7")\n'
    '    pdf.kv("\u6587\u6863\u63a7\u5236", "ISO 13485\u5bf9\u9f50\u7684\u6587\u6863\u751f\u547d\u5468\u671f\u3001\u4fee\u8ba2\u5386\u53f2\u548c\u5ba1\u67e5\u8ba1\u5212")\n'
    '    pdf.kv("\u884c\u52a8\u9879", "\u4efb\u52a1\u770b\u677f\u3001DHF\u6587\u6863\u8ffd\u8e2a\u548cCAPA\u65e5\u5fd7")\n'
    '    pdf.kv("\u65f6\u95f4\u7ebf", "\u6280\u672f\u91cc\u7a0b\u7891\u7684\u5546\u4e1a\u8bed\u8a00\u7ffb\u8bd1")\n'
    '    pdf.kv("\u9884\u7b97", "\u6309\u7c7b\u522b\u7684\u9884\u7b97\u4e0e\u5b9e\u9645\u652f\u51fa")\n'
    '    pdf.kv("\u8d44\u91d1/\u8dd1\u9053", "\u8d22\u52a1\u72b6\u51b5\u3001\u71c3\u70e7\u7387\u3001\u878d\u8d44\u91cc\u7a0b\u7891\u548cAPI\u96c6\u6210")\n'
    '    pdf.kv("\u7f8e\u56fd\u6295\u8d44", "\u5317\u7f8e\u878d\u8d44\u7ba1\u9053\u3001\u6295\u8d44\u8005\u8ffd\u8e2a\u548cIR\u6d3b\u52a8")\n'
    '    pdf.kv("\u8d44\u6e90", "\u56e2\u961f\u5206\u914d\u548c\u4ea7\u80fd\u5229\u7528")\n'
    '    pdf.kv("\u4f9b\u5e94\u5546", "\u786c\u4ef6\u7ec4\u4ef6\u4f9b\u5e94\u5546\u8ffd\u8e2a")\n'
    '    pdf.kv("\u7559\u8a00\u677f", "\u76ee\u6807\u9a71\u52a8\u7684\u7ed3\u6784\u5316\u7ebf\u7a0b\u6d88\u606f\u3001\u51b3\u7b56\u8bb0\u5f55\u3001\u5de5\u4f5c\u6d41\u7b5b\u9009\u548c\u8d23\u4efb\u5236")'
)

if old_cn_kv not in content:
    print("ERROR: CN kv block not found", file=sys.stderr)
    sys.exit(1)
content = content.replace(old_cn_kv, new_cn_kv)
print("1/2 CN tab order updated")

# 2. Add CN section 5.3
old_cn_sec5 = (
    '        "  business " + EM + " \u5546\u4e1a/\u6cd5\u5f8b/\u6295\u8d44\u56e2\u961f\u8d1f\u8d23")\n'
    '\n'
    '    # 6\n'
    '    pdf.add_page()\n'
    '    pdf.sec(6, "\u9009\u9879\u53612\uff1a\u95e8\u63a7\u7cfb\u7edf")'
)

new_cn_sec5 = (
    '        "  business " + EM + " \u5546\u4e1a/\u6cd5\u5f8b/\u6295\u8d44\u56e2\u961f\u8d1f\u8d23")\n'
    '\n'
    '    pdf.sub("5.3 \u91cc\u7a0b\u7891\u8be6\u60c5\u5f39\u7a97")\n'
    '    pdf.txt(\n'
    '        "\u70b9\u51fb\u4efb\u4f55\u91cc\u7a0b\u7891\u5361\u7247\u4f1a\u6253\u5f00\u8be6\u60c5\u5f39\u7a97\uff0c\u663e\u793a\u8def\u5f84\uff08\u6280\u672f\u6216\u6cd5\u89c4\uff09\u3001"\n'
    '        "\u76ee\u6807\u6708\u4efd\u3001\u5f53\u524d\u72b6\u6001\uff0c\u4ee5\u53ca\u91cc\u7a0b\u7891\u8303\u56f4\u548c\u8981\u6c42\u7684\u8be6\u7ec6\u63cf\u8ff0\u3002\\n\\n"\n'
    '        "\u8981\u5173\u95ed\u5f39\u7a97\uff0c\u70b9\u51fb\u5f39\u7a97\u5916\u90e8\u4efb\u4f55\u4f4d\u7f6e\uff08\u53d8\u6697\u7684\u906e\u7f69\u5c42\uff09\u5373\u53ef\u3002"\n'
    '        "\u6ca1\u6709\u5173\u95ed\u6309\u94ae\uff0c\u906e\u7f69\u5c42\u70b9\u51fb\u6a21\u5f0f\u4fdd\u6301\u754c\u9762\u7b80\u6d01\u4e00\u81f4\u3002")\n'
    '\n'
    '    # 6\n'
    '    pdf.add_page()\n'
    '    pdf.sec(6, "\u9009\u9879\u53612\uff1a\u95e8\u63a7\u7cfb\u7edf")'
)

if old_cn_sec5 not in content:
    print("ERROR: CN sec5 block not found", file=sys.stderr)
    sys.exit(1)
content = content.replace(old_cn_sec5, new_cn_sec5)
print("2/2 CN section 5.3 added")

with open('generate_guides.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done - generate_guides.py updated")
