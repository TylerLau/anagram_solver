# Implement Save function (save inputs and results in a log file)
# Implement Load function (load inputs and results from a log file)

import sys
import anagram_solver
from PyQt5.QtWidgets import QMainWindow, QApplication

from Ui_MainWindow import Ui_MainWindow
from dict_map import getKey

# Global dictionary that stores all anagrams parsed from mapped_words.txt
hashmap = {}

# Global that stores max solutions to be found
SOLUTION_LIMIT = 1000

class Anagram_Solver(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUI()

    def initUI(self):
        # Activate SolveFunction when Solve button is clicked
        self.ui.SolveButton.clicked.connect(self.SolveFunction)

        # Activate various functions when menu actions are selected
        self.ui.actionSave.triggered.connect(self.SaveFunction)
        self.ui.actionLoad.triggered.connect(self.LoadFunction)
        self.ui.actionReset.triggered.connect(self.ResetFunction)
        self.ui.actionQuit.triggered.connect(self.QuitFunction)
        self.ui.actionAbout.triggered.connect(self.AboutFunction)

        # Set action menu shortcuts
        self.ui.actionSave.setShortcut("Ctrl+S")
        self.ui.actionLoad.setShortcut("Ctrl+L")
        self.ui.actionQuit.setShortcut("Ctrl+Q")

        self.show()

    def SolveFunction(self):
        # Collect input string and calculate its key value
        input = str(self.ui.InputString.toPlainText()).strip()
        input_key = getKey(input)

        # Collect list of required words and check if they are valid
        required = list(map(str.strip, str(self.ui.RequiredWords.toPlainText()).split(',')))
        input_key = anagram_solver.checkWords(input_key, required)
        if input_key == -1:
            self.ui.OutputList.clear()
            self.ui.OutputList.addItem("Required words not in input string")
            return

        # Collect min/max length inputs and check if they are valid
        min_s = str(self.ui.MinValue.currentText())
        max_s = str(self.ui.MaxValue.currentText())
        min = -1 if min_s == "(none)" else int(min_s)
        max =  -1 if max_s == "(none)" else int(max_s)

        if max < min and not max == -1:
            self.ui.OutputList.clear()
            self.ui.OutputList.addItem("Max length is less than min length")
            return

        # Create trimmed dictionary from constraints
        trimmed_dict = anagram_solver.trimDictionary(hashmap, input_key, min, max)

        # Reset the progress bar and output list
        solution_counter, progress_counter = 0, 0
        progress_max = len(trimmed_dict)
        self.ui.ProgressBar.setValue(0)
        self.ui.ProgressBar.setMaximum(progress_max)
        self.ui.OutputList.clear()
        QApplication.processEvents()

        # Start solving the anagrams
        for key in trimmed_dict.copy():
            for word in trimmed_dict[key]:
                word_list = anagram_solver.solveHelper(trimmed_dict, input_key/key, required + [word])
                if word_list:
                    for sol in word_list:
                        solutions = anagram_solver.StringMaker(sol)
                        for s in solutions:
                            self.ui.OutputList.addItem(s)
                            solution_counter += 1

                            if solution_counter >= SOLUTION_LIMIT:
                                break
                        if solution_counter >= SOLUTION_LIMIT:
                            break
                if solution_counter >= SOLUTION_LIMIT:
                    break
            if solution_counter >= SOLUTION_LIMIT:
                break

            trimmed_dict.pop(key)
            progress_counter += 1
            self.ui.ProgressBar.setValue(progress_counter)
            QApplication.processEvents()

        # Fill up progress bar if loop ended early for 1000 solution limit
        if not progress_counter == progress_max:
            self.ui.ProgressBar.setValue(progress_max)
            QApplication.processEvents()

    def SaveFunction(self):
        print("saved")

    def LoadFunction(self):
        print("loaded")

    def ResetFunction(self):
        print("reset")
        self.ui.OutputList.clear()
        self.ui.InputString.clear()
        self.ui.RequiredWords.clear()
        self.ui.MinValue.setCurrentIndex(0)
        self.ui.MaxValue.setCurrentIndex(0)
        self.ui.ProgressBar.setValue(0)
        QApplication.processEvents()

    def QuitFunction(self):
        print("quitting")
        QApplication.quit()

    def AboutFunction(self):
        print("about")

if __name__ == '__main__':
    # Set up the dictionary
    hashmap = anagram_solver.initHash()

    # Start the UI
    app = QApplication(sys.argv)
    ex = Anagram_Solver()
    sys.exit(app.exec_())
