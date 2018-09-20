# This is the main file
# 
# This calculator can do addition, subtract, multiplication, division, and calculate percent
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
# 

import PySimpleGUI as sg


class Calculator:

    def __init__(self):
        self.temp = 0
    
    def onExec(self):
        """On executing"""

        buttons = [["C", "%", "del", "÷"],
                   ["7", "8", "9", "×"],
                   ["4", "5", "6", "-"],
                   ["1", "2", "3", "+"],
                   ["+/-", "0", ".", "="]]
        col = 4
        row = 5

        form = sg.FlexForm("PySimpleCalculator", auto_size_text=True, auto_size_buttons=False, default_element_size=(40, 1), default_button_element_size=(4, 1), scale=(1, 1), background_color="#222631")
        layout = [[sg.Text(self.temp, size=(15, 3), font=("Consolas", 30), justification="right", text_color="white", background_color="#222631")]]
        
        for i in range(row):
            res = []
            for j in range(col):
                if buttons[i][j] == "del":
                    res.append(sg.ReadFormButton(buttons[i][j], image_filename="icon/outline_backspace_white_18dp.png", image_size=(78, 63), image_subsample=1, button_color=("white", "#4a5163"), font=("Consolas", 25)))
                else:
                    res.append(sg.ReadFormButton(buttons[i][j], button_color=("white", "#4a5163"), font=("Consolas", 25)))
            layout.append(res)

        button, values = form.LayoutAndRead(layout)
        # sg.Popup(button, values)


if __name__ == "__main__":
    app = Calculator()
    app.onExec()