# This class is used to control this program
# (it the same class in https://github.com/nutchun/PyCalculator)
# e.g. calculate an equation
# 
# You can visit my repository at
# https://github.com/nutchun/PySimpleCalculator
# 
# This project is a part of Software Development Practice 1 course
#
# Developed by Nuttakan Chuntra
# Computer Engineering student at KMUTNB
# Student ID: 5901012630032
# Bangkok, Thailand
# Email: nut.ch40@gmail.com

import operator

class Controller:
    """Control almost everything in calculator"""

    def __init__(self):
        self.equation = []
        self.temp = ""
        self.operators = ("+", "-", "×", "÷", "xʸ")
        self.opers = {"+": "+", "-": "-", "×": "*", "÷": "/", "xʸ": "^"}
        self.numbers = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        self.currentInput = None
        self.parentheses = 0
        self.reset = False
        self.keydown = False
        self.inputLength = 0
        self.maxchar = 1
    
    @property
    def temps(self):
        return self.temp
    
    @temps.setter
    def temps(self, temp):
        self.temp += temp

    def getEquation(self):
        return self.temp

    def setInputLength(self, length):
        self.inputLength = length
    
    def setMaxChar(self, maxchar):
        self.maxchar = maxchar

    def addInput(self, input):
        self.currentInput = input
    
    def resetInput(self):
        self.currentInput = None

    def onHover(self, rect, bound, ):
        pass

    def onKeyDown(self):
        self.keydown = True

    def onCalculate(self, equation):
        """Calculate long equation"""

        pointer = -1
        negate = False
        sqrt = False

        while pointer > -len(equation) - 1:
            if equation[pointer] == ")":
                parenthRight = pointer
                while equation[pointer][-1] != "(":
                    pointer -= 1
                    if equation[pointer] == ")":
                        parenthRight = pointer
                if equation[pointer] == "-(":
                    negate = True
                elif equation[pointer] == "√(":
                    sqrt = True
                parenthLeft = pointer
                result = self.sequenceCalculate(equation[parenthLeft + 1:parenthRight])
                if negate:
                    result = str(self.toNumber(result) * -1)
                elif sqrt:
                    result = str(self.toNumber(result) ** 0.5)
                for i in range(len(equation[parenthLeft:parenthRight])):
                    equation.pop(parenthLeft + i)
                equation[parenthRight] = result
                pointer = 0
                negate = False
                sqrt = False
            pointer -= 1
        
        result = 0
        # check for real float or integer
        if len(equation) == 1:
            # need not to searching for parentheses again
            try:
                if float(equation[0]).is_integer():
                    result = self.checkInt(float(equation[0]))
                else:
                    result = self.checkInt(float(equation[0]))
            except ValueError:
                # result = "Error: Does not support complex numbers"
                result = complex(equation[0])
        else:
            try:
                if float(self.sequenceCalculate(equation)).is_integer():
                    result = self.checkInt(float(self.sequenceCalculate(equation)))
                else:
                    result = self.checkInt(float(self.sequenceCalculate(equation)))
            except ValueError:
                # result = "Error: Does not support complex numbers"
                result = complex(equation[0])
        return result

    def toNumber(self, string):
        """Return real integer or float"""
        try:
            if "." in string:
                try:
                    return float(string)
                except ValueError:
                    # if isinstance(string, complex):
                    #     print("Error: Does not support imaginary number")
                    raise
            return int(string)
        except ValueError:
            print("Invalid value")
            raise

    def getOperator(self, oper):
        """Return operator function"""
        return {
            "+": operator.add,
            "-": operator.sub,
            "×": operator.mul,
            "÷": operator.truediv,
            "xʸ": operator.pow
        }[oper]

    def calculate(self, op1, oper, op2):
        """Return the result that calculated by two numbers"""
        return self.getOperator(oper)(self.toNumber(op1), self.toNumber(op2))

    def sequenceCalculate(self, equation):
        """Return the result depending on the order of mathematical operators"""
        order = ("xʸ", "÷", "×", "-", "+")
        n = 0
        for i in order:
            while n < len(equation):
                if i == equation[n]:
                    num1 = equation[n - 1]
                    oper = equation[n]
                    num2 = equation[n + 1]
                    result = self.calculate(num1, oper, num2)
                    equation[n + 1] = str(result)
                    equation.pop(n - 1)
                    equation.pop(n - 1)
                    n = 0
                else:
                    n += 1
            n = 0
        return equation[0]

    def checkInt(self, num):
        """Check if float is integer"""
        if num.is_integer():
            return int(num)
        return num
    
    def getResult(self):
        try:
            if self.equation[-1] in self.operators or self.equation[-1] == "xʸ":
                self.equation.pop()
            if self.parentheses > 0:
                for i in range(self.parentheses):
                    self.equation.append(")")
                    self.parentheses -= 1
            result = self.onCalculate(self.equation)
            # if isinstance(result, complex):
            #     result = complex()
            self.equation = [str(result)]
        except IndexError:
            self.equation = ["Invalid input"]
        except ValueError:
            self.equation = ["Invalid input"]
        except ZeroDivisionError:
            self.equation = ["Error: Division by zero"]
        except:
            self.equation = []
        finally:
            self.reset = True
    
    def addNumber(self):
        if self.equation[-1] in self.operators or self.equation[-1] == "-(" or self.equation[-1] == "(" or self.equation[-1] == "√(":
            self.equation.append(self.currentInput)
        elif self.equation[-1] == ")":
            while self.equation[-1] not in ["(", "-(", "√("]:
                if self.equation[-1] == ")":
                    self.parentheses += 1
                self.equation.pop()
            self.equation.append(self.currentInput)
            # self.parentheses += 1
        elif self.equation[-1] == "0":
            self.equation[-1] = self.currentInput
        else:
            self.equation[-1] += self.currentInput
    
    def addDecPoint(self):
        if self.equation[-1] in self.operators:
            self.equation.append("0.")
        elif self.equation[-1] == "(" or self.equation[-1] == "-(" or self.equation[-1] == "√(":
            self.equation.append("0.")
        elif self.equation[-1] == ")":
            self.equation.append("×")
            self.equation.append(self.currentInput)
        elif self.currentInput not in self.equation[-1]:
            self.equation[-1] += self.currentInput
    
    def addOperator(self):
        if self.equation[-1] in self.operators:
            self.equation[-1] = self.currentInput
        elif self.equation[-1][-1] == ".":
            if self.equation[-1][:-1] != "0":
                self.equation[-1] = self.equation[-1][:-1]
                self.equation.append(self.currentInput)
            else:
                try:
                    if self.equation[-2] == "+" or self.equation[-2] == "-":
                        self.equation.pop()
                        self.equation.pop()
                        self.equation.append(self.currentInput)
                except IndexError:
                    self.equation.pop()
        elif self.equation[-1] == "(" or self.equation[-1] == "-(" or self.equation[-1] == "√(":
            try:
                while self.equation[-1] not in self.operators:
                    self.equation.pop()
                    self.parentheses -= 1
                self.equation.pop()
                self.equation.append(self.currentInput)
            except IndexError:
                pass
        else:
            self.equation.append(self.currentInput)

    def addPlusMinus(self):
        if self.equation[-1] in self.operators or self.equation[-1] == "(" or self.equation[-1] == "-(" or self.equation[-1] == "√(":
            self.equation.append("-(")
            self.parentheses += 1
        elif self.equation[-1] == ")":
            self.equation.append("×")
            self.equation.append("-(")
            self.parentheses += 1
        else:
            self.equation[-1] = str(self.checkInt(float(self.equation[-1]) * -1))

    def addOpenedParenthesis(self):
        if self.equation[-1] in self.operators or self.equation[-1] == "(" or self.equation[-1] == "-(" or self.equation[-1] == "√(":
            self.equation.append(self.currentInput)
            self.parentheses += 1
        elif self.equation[-1] == ")":
            self.equation.pop()
            self.parentheses += 1
        else:
            res = self.equation[-1]
            self.equation[-1] = self.currentInput
            self.equation.append(res)
            # self.equation.append("×")
            # self.equation.append(self.currentInput)
            self.parentheses += 1

    def addClosedParenthesis(self):
        if self.equation[-1] == "(" or self.equation[-1] == "-(" or self.equation[-1] == "√(":
            self.equation.pop()
            self.parentheses -= 1
        elif self.parentheses != 0:
            if self.equation[-1] in self.operators:
                self.equation.pop()
            self.equation.append(self.currentInput)
            self.parentheses -= 1
    
    def addSqrt(self):
        if self.equation[-1] == ")":
            left = 0
            n = 0
            for i in range(-1, -len(self.equation) - 1, -1):
                if self.equation[i] == ")":
                    n += 1
                elif self.equation[i] == "(" or self.equation[i] == "-(" or self.equation[i] == "√(":
                    n -= 1
                    left = i
                if n == 0 and left != 0:
                    left = i
                    break
            res = self.equation[left:]
            self.equation = self.equation[:left]
            self.equation.append("√(")
            self.equation += res
            self.equation.append(")")
        elif not (self.equation[-1] in self.operators or self.equation[-1] == "(" or self.equation[-1] == "-(" or self.equation[-1] == "√("):
            num = self.equation[-1]
            self.equation[-1] = "√("
            self.equation.append(num)
            self.equation.append(")")
        else:
            # if not (self.equation[-1] in self.operators or self.equation[-1] == "(" or self.equation[-1] == "-(" or self.equation[-1] == "√("):
            #     self.equation.append("×")
            self.equation.append("√(")
            self.parentheses += 1
    
    def addPercent(self):
        if len(self.equation) > 2:
            left = 0
            if self.equation[-1] == ")":
                # left = 0
                n = 0
                for i in range(-1, -len(self.equation) - 1, -1):
                    if self.equation[i] == ")":
                        n += 1
                    elif self.equation[i] == "(" or self.equation[i] == "-(" or self.equation[i] == "√(":
                        n -= 1
                        left = i
                    if n == 0 and left != 0:
                        left = i
                        break
                num = self.equation[left:]
                oper = self.equation[left - 1]
            else:
                num = [self.equation[-1]]
                oper = self.equation[-2]
                left = -1
            res = ""
            right = left - 1
            if self.equation[left - 2] == ")":
                # left = 0
                n = 0
                for i in range(left - 2, -len(self.equation) - 1, -1):
                    if self.equation[i] == ")":
                        n += 1
                    elif self.equation[i] == "(" or self.equation[i] == "-(" or self.equation[i] == "√(":
                        n -= 1
                        left = i
                    if n == 0 and left != 0:
                        left = i
                        break
                res = self.equation[left:right]
            else:
                res = [self.equation[right - 1]]
            if oper == "+" or oper == "-":
                self.equation = self.equation[:right + 1]
                eq = res + ["×"] + num + ["÷"] + ["100"]
                self.equation += [str(self.onCalculate(eq))]
            elif oper == "×" or oper == "÷" or oper == "xʸ":
                self.equation.append("÷")
                self.equation.append("100")
        else:
            if self.equation[-1] not in self.operators and self.equation[-1] != "(" and self.equation[-1] != "-(" and self.equation[-1] != "√(":
                self.equation.append("÷")
                self.equation.append("100")
    
    def formatEquation(self, equation):
        temp = ""
        if equation:
            for i in equation:
                if i in self.operators:
                    temp += " " + i + " "
                else:
                    temp += i
        else:
            return "0"
        return temp

    def popEquation(self):
        if self.equation[-1] in self.operators or self.equation[-1] == "+/-":
            self.equation.pop()
        elif self.equation[-1] == "(" or self.equation[-1] == "-(" or self.equation[-1] == "√(":
            self.equation.pop()
            self.parentheses -= 1
        elif self.equation[-1] == ")":
            self.equation.pop()
            self.parentheses += 1
        else:
            self.equation[-1] = self.equation[-1][:-1]
            if not self.equation[-1]:
                self.equation.pop()

    def onHandle(self):
        """Handle the input"""

        if self.reset and self.currentInput in self.numbers:
            self.equation = []
            self.reset = False
        elif self.currentInput != None:
            self.reset = False

        # empty list state
        if not self.equation:
            if self.currentInput in self.numbers:
                self.equation.append(self.currentInput)
            elif self.currentInput == ".":
                self.equation.append("0.")
            elif self.currentInput in self.operators:
                self.equation.append("0")
                self.equation.append(self.currentInput)
            elif self.currentInput == "(":
                self.equation.append(self.currentInput)
                self.parentheses += 1
            elif self.currentInput == "+/-":
                self.equation.append("-(")
                self.parentheses += 1
            elif self.currentInput == "√x":
                self.equation.append("√(")
                self.parentheses += 1
            # elif self.currentInput == "del" or self.currentInput == "AC" or self.currentInput == "C":
                # self.temp = "0"
            # self.temp = " ".join(self.equation)

        # not empty
        else:
            ##################################################
            # when clear
            if self.currentInput == "AC" or self.currentInput == "C":
                self.equation = []
                self.parentheses = 0
            
            ##################################################
            # when pressed backspace
            elif self.currentInput == "del":
                self.popEquation()
            
            ##################################################
            elif self.currentInput == "=":
                self.getResult()
            
            # prevent user to insert input if its length more than 42 chars
            if self.inputLength < self.maxchar:

                ##################################################
                # when insert numbers
                if self.currentInput in self.numbers:
                    self.addNumber()
                
                ##################################################
                # when insert a decimal point
                elif self.currentInput == ".":
                    self.addDecPoint()
                
                ##################################################
                # when insert operators
                elif self.currentInput in self.operators:
                    self.addOperator()
                
                ##################################################
                # when toggle between positive and negertive value
                elif self.currentInput == "+/-":
                    self.addPlusMinus()
                
                ##################################################
                # when insert open parenthesis
                elif self.currentInput == "(":
                    self.addOpenedParenthesis()
                
                ##################################################
                # when insert close parenthesis
                elif self.currentInput == ")":
                    self.addClosedParenthesis()
                    
                ##################################################
                # when insert square root sign
                elif self.currentInput == "√x":
                    self.addSqrt()
                
                ##################################################
                # when insert percent sign
                elif self.currentInput == "%":
                    self.addPercent()
        
        # always reset input to None
        self.resetInput()
        
        return self.formatEquation(self.equation), self.reset
