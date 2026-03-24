#!/usr/bin/env python3
"""Temporary script to update generate_guides.py CN section for Message Board rename."""

with open("generate_guides.py", "r", encoding="utf-8") as f:
    content = f.read()

count = 0

# The file uses \uXXXX escape sequences in string literals.
# We need to match those exact sequences.

# Fix double replacement: \u7559\u8a00\u677f\u7559\u8a00\u677f -> \u7559\u8a00\u677f
# (This happened because the first script replaced 发明人问答留言板 -> 留言板 globally,
#  but the sec() title was "选项卡14：发明人问答留言板" which became "选项卡14：留言板留言板")
old = r"\u9009\u9879\u530114\uff1a\u7559\u8a00\u677f\u7559\u8a00\u677f"
new = r"\u9009\u9879\u530114\uff1a\u7559\u8a00\u677f"
if old in content:
    content = content.replace(old, new)
    count += 1
    print(f"Fixed: sec() title double-replacement")

# Replace 发明人 with 戴博士 in unicode escape sequences
# \u53d1\u660e\u4eba = 发明人
# \u6234\u535a\u58eb = 戴博士

# PMP与发明人之间
old = r"\u4e0e\u53d1\u660e\u4eba\u4e4b\u95f4"
new = r"\u4e0e\u6234\u535a\u58eb\u4e4b\u95f4"
if old in content:
    n = content.count(old)
    content = content.replace(old, new)
    count += n
    print(f"Replaced 与发明人之间 -> 与戴博士之间 ({n}x)")

# PMP和发明人之间切换
old = r"\u548c\u53d1\u660e\u4eba\u4e4b\u95f4\u5207\u6362"
new = r"\u548c\u6234\u535a\u58eb\u4e4b\u95f4\u5207\u6362"
if old in content:
    n = content.count(old)
    content = content.replace(old, new)
    count += n
    print(f"Replaced 和发明人之间切换 -> 和戴博士之间切换 ({n}x)")

# 一个作发明人
old = r"\u4e00\u4e2a\u4f5c\u53d1\u660e\u4eba"
new = r"\u4e00\u4e2a\u4f5c\u6234\u535a\u58eb"
if old in content:
    n = content.count(old)
    content = content.replace(old, new)
    count += n
    print(f"Replaced 一个作发明人 -> 一个作戴博士 ({n}x)")

# 和发明人邮箱
old = r"\u548c\u53d1\u660e\u4eba\u90ae\u7bb1"
new = r"\u548c\u6234\u535a\u58eb\u90ae\u7bb1"
if old in content:
    n = content.count(old)
    content = content.replace(old, new)
    count += n
    print(f"Replaced 和发明人邮箱 -> 和戴博士邮箱 ({n}x)")

# 留言板提供...发明人 (already handled as 留言板 above,
# but the body text still says 发明人)
# The txt body: "\u7559\u8a00\u677f\u63d0\u4f9b...PMP)\u4e0e\u53d1\u660e\u4eba..."
# After the \u4e0e replacement above, this should already be fixed.

with open("generate_guides.py", "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nTotal replacements: {count}")
