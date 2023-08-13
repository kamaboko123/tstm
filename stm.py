import argparse
import logging
import sys
import re
import traceback
from gui import StackView

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Stm:
    def __init__(self):
        self.stack_max = 1000
        self.program_max = 1000
        self.stack = [None for i in range(self.stack_max)]
        self.program = [[] for i in range(self.program_max)]
        self.pc = 0
        self.a = 0
        self.b = 0
        self.bp = self.stack_max - 2
        self.sp = self.stack_max - 2
 
    def parse(self, line):
        line_parse = line.split(" ")
        line_no = int(line_parse[0])
        line_op = line_parse[1]
        line_arg1 = int(line_parse[2]) if len(line_parse) >= 3 else None

        return (line_no, line_op, line_arg1)

    def set_program(self, lines):
        for line in lines:
            if re.match("^#", line) or not line:
                continue
            self.set_line(*self.parse(line))

    def set_line(self, line_no, line_op, line_arg1):
        logger.debug(f"{line_no}, {line_op}, {line_arg1}")
        self.program[line_no] = [line_op, line_arg1]

    def dump_program(self):
        for line_no, line in enumerate(self.program):
            if line == []:
                continue
            print(line_no, line)

    def dump_stack(self):
        print("=== stack dump ===")
        for i in range(self.sp, self.stack_max):
            data = self.stack[i]
            if data is None:
                data = "null"
            else:
                data = "%04d" % data
            print("%04d | %08s | %04s" % (i, data, "*bp" if self.bp == i else ""))
        print("==================")

    # 以下は実際の命令の実行処理
    def step(self):
        inst = self.program[self.pc]
        self.pc += 1
        
        if inst == [] or inst[0] == "nop":
            self._nop()

        elif inst[0] == "push":
            self._push(inst[1])

        elif inst[0] == "pop":
            self._pop()
        
        elif inst[0] == "add":
            self._add()
        
        elif inst[0] == "sub":
            self._sub()

        elif inst[0] == "mul":
            self._mul()
        
        elif inst[0] == "div":
            self._div()
        
        elif inst[0] == "mod":
            self._mod()
        
        elif inst[0] == "jmp":
            self._jmp(inst[1])
        
        elif inst[0] == "call":
            self._call(inst[1])
        
        elif inst[0] == "enter":
            self._enter()

        elif inst[0] == "ret":
            self._ret()

        elif inst[0] == "popr":
            self._popr(inst[1])
        
        elif inst[0] == "storel":
            self._storel(inst[1])

        elif inst[0] == "loadl":
            self._loadl(inst[1])
        
        elif inst[0] == "storea":
            self._storea(inst[1])
        
        elif inst[0] == "loada":
            self._loada(inst[1])

        elif inst[0] == "exit":
            return False

        elif inst[0] == "print":
            self._print()
        
        elif inst[0] == "beqz":
            self._beqz(inst[1])
        
        elif inst[0] == "bnqz":
            self._bnqz(inst[1])

        self.skip_blank()
        return True

    def skip_blank(self):
        while self.program[self.pc] == []:
            self.pc += 1

    def _nop(self):
        pass

    def _push(self, data):
        self.sp -= 1
        self.stack[self.sp] = data
    
    def _pop(self):
        data = self.stack[self.sp]
        self.sp += 1
        return data

    def _add(self):
        self.a = self._pop()
        self.b = self._pop()
        self.a += self.b
        self._push(self.a)
    
    def _sub(self):
        self.b = self._pop()
        self.a = self._pop()
        self.a -= self.b
        self._push(self.a)
    
    def _mul(self):
        self.a = self._pop()
        self.b = self._pop()
        self.a *= self.b
        self._push(self.a)

    def _div(self):
        self.b = self._pop()
        self.a = self._pop()
        self.a //= self.b
        self._push(self.a)

    def _mod(self):
        self.b = self._pop()
        self.a = self._pop()
        self.a %= self.b
        self._push(self.a)

    def _jmp(self, next_line):
        self.pc = next_line

    def _call(self, next_line):
        self._push(self.pc)
        self.pc = next_line

    def _enter(self):
        self._push(self.bp)
        self.bp = self.sp

    def _ret(self):
        self.a = self._pop()
        self.bp = self._pop()
        self.pc = self._pop()
        self._push(self.a)

    def _popr(self, n):
        self.a = self._pop()
        self.sp += n
        self._push(self.a)

    def _storel(self, n):
        self.a = self._pop()
        self.stack[self.bp - n] = self.a

    def _loadl(self, n):
        self._push(self.stack[self.bp - n])
    
    def _storea(self, n):
        self.a = self._pop()
        self.stack[self.bp + 1 + n] = self.a
    
    def _loada(self, n):
        self._push(self.stack[self.bp + 1 + n])
    
    def _print(self):
        print(self.stack[self.sp])
    
    def _beqz(self, next_line):
        self.a = self._pop()
        if self.a == 0:
            self.pc = next_line
    
    def _bnqz(self, next_line):
        self.a = self._pop()
        if self.a != 0:
            self.pc = next_line



def read_program(filename):
    with open(filename, "r") as f:
        program = f.read().splitlines()
    
    return program


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tiny Stack Machine")
    parser.add_argument("program_file_name", type=str, help="実行するプログラムファイル")
    parser.add_argument("-i", "--interactive", action='store_true', help="インタラクティブモード")
    parser.add_argument("-d", "--debug", action='store_true', help="スタックビューアーを表示します")
    args = parser.parse_args()

    prog = read_program(sys.argv[1])

    stm = Stm()
    stm.set_program(prog)
    #stm.dump_program()

    if args.debug:
        import tkinter
        gui = tkinter.Tk()
        stack_view = StackView(gui, stm)

    try:
        if args.interactive:
            while True:
                print(f"pc: {stm.pc}")
                print(f"next exec: {stm.program[stm.pc]}")

                op = input("> ")
                if op.isdecimal():
                    for _i in range(int(op)):
                        stm.step()
                elif op in ["d", "dump"]:
                    stm.dump_stack()
                elif op in ["e", "exit"]:
                    break
                elif op in ["n", "next"]:
                    state = stm.step()
                    if not state:
                        break
                else:
                    print("d | dump :  Dump stack")
                    print("e | exit :  Exit program")
                    print("n | next :  Execute Next Step")
                if args.debug:
                    stack_view.update()
                print()
        else:
            while True:
                state = stm.step()
                if not state:
                    break
                if args.debug:
                    stack_view.update()
    except Exception:
        traceback.print_exc()
        sys.stderr.write(f"pc: {stm.pc}\n")
        sys.exit(1)

    sys.exit(0)


