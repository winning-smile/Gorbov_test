Black = "rgba(20, 20, 20, 1)"
Red = "rgba(201, 44, 44, 1)"

black_default = """
background-color: rgba(20, 20, 20, 1);
max-height: 60px;
max-width: 60px;
margin: 0px;
padding: 15px;
color: white;
font-size: 40px;
border: 3px solid rgba(20, 20, 20, 1);
border-radius: 15px;
"""


red_default = """
background-color: rgba(201, 44, 44, 1);
max-height: 60px;
max-width: 60px;
margin: 0px;
padding: 15px;
color: white;
font-size: 40px;
border: 3px solid rgba(201, 44, 44, 1);
border-radius: 15px;
"""


black_white = """QPushButton {
              background-color: white;
              max-height: 60px;
              max-width: 60px;
              margin: 0px;
              padding: 15px;
              color: rgba(20, 20, 20, 1);
              font-size: 40px;
              border-radius: 15px;
              }
              QPushButton::hover {
              background-color: rgba(170, 170, 170, 1);
              }"""


red_white = """QPushButton {
            background-color: white;
            max-height: 60px;
            max-width: 60px;
            margin: 0px;
            padding: 15px;
            color: rgba(201, 44, 44, 1);
            font-size: 40px;
            border-radius: 15px;
            }
            QPushButton::hover {
            background-color: rgba(170, 170, 170, 1);
            }"""

menu_button = """QPushButton {
            background-color: white;
            min-height: 30px;
            min-width: 150px;
            color: rgba(20, 20, 20, 1);
            border-radius: 5px;
            font-weight: 900;
            }
            QPushButton::hover {
            background-color: rgba(150, 150, 150, 1);
            }
            QPushButton::pressed {
            border: 2px solid rgba(110, 110, 110, 1);
            }
            QPushButton::disabled {
            background-color: rgba(110, 110, 110, 1);
            }"""

menu_lines = """QLineEdit{
            background-color: white;
            min-height: 30px;
            max-width: 300px;
            color: rgba(20, 20, 20, 1);
            border-radius: 5px;
            font-weight: 900;
            }
            QLineEdit::hover {
            background-color: rgba(150, 150, 150, 1);
            }
            QLineEdit::pressed {
            border: 2px solid rgba(110, 110, 110, 1);
            }
            QLineEdit::disabled {
            background-color: rgba(110, 110, 110, 1);
            }"""
