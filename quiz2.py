import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QRadioButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore
import requests
import json
import random
import html
from PyQt5.QtCore import Qt, QEvent


class Quiz(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz")
        self.setFixedSize(1000, 1000)
        self.score = 0
        self.questions = []
        self.question_num = 0
        self.create_widgets()
        self.get_questions()
        self.setStyleSheet("background-color: gray;")
        self.submit_button.setStyleSheet("background-color: green; color: white; border-radius: 10px; padding: 10px;")
        self.submit_button.installEventFilter(self)


    def create_widgets(self):
        """ self.title_label = QLabel("Welcome to the Quiz!", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 20)) """

        self.question_label = QLabel("", self)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setFont(QFont("Arial", 16))
        self.question_label.setWordWrap(True)
        self.question_label.setMaximumWidth(1000)

        self.answer_a = QRadioButton("", self)
        self.answer_a.setFont(QFont("Arial", 14))

        self.answer_b = QRadioButton("", self)
        self.answer_b.setFont(QFont("Arial", 14))

        self.answer_c = QRadioButton("", self)
        self.answer_c.setFont(QFont("Arial", 14))

        self.answer_d = QRadioButton("", self)
        self.answer_d.setFont(QFont("Arial", 14))


        self.answer_buttons = [self.answer_a, self.answer_b, self.answer_c, self.answer_d]

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.setFixedSize(1000, 100)
        self.submit_button.clicked.connect(self.check_answer)
        self.submit_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.submit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.layout = QVBoxLayout()
        #self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.question_label)
        self.layout.addWidget(self.answer_a)
        self.layout.addWidget(self.answer_b, 1)
        self.layout.addWidget(self.answer_c)
        self.layout.addWidget(self.answer_d)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def get_questions(self):
        api_endpoint = "https://opentdb.com/api.php?amount=10&category=27&difficulty=easy&type=multiple"
        params = {
            "amount": 10,
            "difficulty": "easy",
            "type": "multiple"
        }
        response = requests.get(api_endpoint, params=params)
        data = json.loads(response.text)
        self.questions = data["results"]
        self.show_question()

    def show_question(self):
        question = self.questions[self.question_num]
        question_text = html.unescape(question['question'])
        self.question_label.setText(question_text)

        answers = question["incorrect_answers"] + [question["correct_answer"]]
        random.shuffle(answers)

        for i, answer in enumerate(answers):
            answer_text = html.unescape(answer)
            self.answer_buttons[i].setText(answer_text)
            self.answer_buttons[i].setChecked(False)

    def check_answer(self):
        selected_answer = None
        for i, answer_button in enumerate(self.answer_buttons):
            if answer_button.isChecked():
                selected_answer = i
                break

        if selected_answer is None:
            QMessageBox.warning(self, "Error", "Please select an answer.")
            return

        question = self.questions[self.question_num]
        if question["correct_answer"] == html.unescape(self.answer_buttons[selected_answer].text()):
            QMessageBox.information(self, "Correct", "Your answer is correct!")
            self.score += 1
        else:
            correct_answer_text = html.unescape(question['correct_answer'])
            QMessageBox.information(self, "Incorrect", f"Your answer is incorrect. The correct answer is {correct_answer_text}.")

        self.question_num += 1
        if self.question_num < len(self.questions):
            self.show_question()
        else:
            QMessageBox.information(self, "Quiz Complete", f"Your final score is {self.score}/{len(self.questions)}.")
            self.close()
    
    def eventFilter(self, object, event):
        if event.type() == QEvent.HoverEnter:
            if object == self.submit_button:
                object.setStyleSheet("background-color: blue; color: white; border-radius: 10px; padding: 10px;")
        elif event.type() == QEvent.HoverLeave:
            if object == self.submit_button:
                object.setStyleSheet("background-color: gray; color: white; border-radius: 10px; padding: 10px;")
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    quiz = Quiz()
    quiz.show()
    sys.exit(app.exec_())
