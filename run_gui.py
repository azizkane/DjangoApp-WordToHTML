# py manage.py runserver before everything else
# then run as python file

from gui.main_window import WordToHtmlGUI

if __name__ == "__main__":
    app = WordToHtmlGUI()
    app.run()
