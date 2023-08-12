import sys

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


def move_output(output, buf):
    while len(buf) > 0:
        data = buf.pop()
        if data == "(":
            break
        elif data == ")":
            continue
        output.append(data)

def convert(infix):
    rpn_output = []
    operator_buffer = []
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

    return rpn_output


if __name__ == "__main__":
    infix = sys.argv[1].split()
    rpn = convert(infix)

    print("IN expression: %s" % " ".join(infix))
    print("RPN expression: %s" % " ".join(rpn))
    
    print("[STML]")
    line_no = 10
    for token in rpn:
        if token.isdecimal():
            print(f"{line_no} push {token}")
        else:
            print(f"{line_no} {operator_convert_table[token]}")
        
        line_no += 10
    print(f"{line_no + 10} print")
    print(f"{line_no + 20} exit")
