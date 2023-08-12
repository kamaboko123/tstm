import sys

infix = sys.argv[1]
rpn_output = []
operator_buffer = []

operator_priority = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "(": 0,
    ")": 0,
}

operator_convert_table = {
    "+": "add",
    "-": "sub",
    "*": "mul",
    "/": "div"
}

infix = infix.split()

def move_output(output, buf):
    while len(buf) > 0:
        data = buf.pop()
        if data == "(":
            break
        elif data == ")":
            continue
        output.append(data)

for token in infix:
    # 数値はそのまま出力
    if token.isdecimal():
        rpn_output.append(token)
    
    elif token in operator_priority.keys():
        if token == "(":
            pass
        elif token == ")":
            # 閉じ括弧が出てきたらすべて出力(それまでの計算を確定させる)
            move_output(rpn_output, operator_buffer)
        elif len(operator_buffer) > 0 and operator_priority[token] < operator_priority[operator_buffer[-1]]:
            # 優先度の高い演算子がバッファに入っていたら先にバッファの中を出力
            move_output(rpn_output, operator_buffer)
        operator_buffer.append(token)

# バッファに残った演算子をすべてを出力
move_output(rpn_output, operator_buffer)

print("IN expression: %s" % " ".join(infix))
print("RPN expression: %s" % " ".join(rpn_output))
