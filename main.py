import math
import os
import random
import re
import shutil
import string
import sys
import tkinter as tk
from _pydecimal import Decimal
from math import floor
from tkinter import filedialog

import aspose.words as bw
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import pypandoc
# import tokenizer as tokenizer
from PyQt5.QtGui import QFont
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from nltk.stem import PorterStemmer
from nltk.tag import pos_tag
from nltk.tokenize import RegexpTokenizer, sent_tokenize
from nltk.tokenize import word_tokenize
from rouge_score import rouge_scorer

from sentence_transformers import SentenceTransformer
from nltk.corpus import stopwords
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from rouge import Rouge
import os

os.environ.setdefault('PYPANDOC_PANDOC', '/home/x/whatever/pandoc')


# noinspection PyArgumentList


class MyWindow(QWidget):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.send = None
        self.win2 = None
        self.generalPath = None
        self.path = None
        self.file_path = None
        self.filename = None
        self.lbl_name = QLabel(self)
        self.lbl_path = QLabel(self)
        self.openFileExplorer = QPushButton(self)
        self.saveFile = QPushButton(self)
        self.saveFileSummary = QPushButton(self)
        self.createGraph = QPushButton(self)
        self.message = QMessageBox(self)
        self.setGeometry(1200, 300, 700, 700)
        self.setWindowTitle('Main Page')
        self.initUi()

    def FeClicking(self):  # Dosya ismi alınıyor pathten
        root = tk.Tk()
        root.withdraw()
        self.file_path = filedialog.askopenfilename()
        self.lbl_path.setText(self.file_path)
        self.filename = self.file_path.split('/')[-1]
        print('Dosya Yolu', self.file_path)
        print('Dosya ismi', self.filename)

    def Create_Graph(self):

        self.win2 = SetGraphWindow()
        self.win2.show()
        self.hide()

    def FsClicking(self):

        path1 = "C:\\Users\\sulta\\PycharmProjects\\GraphApplication\\Document\\"
        count = 0
        list = os.listdir(path1)
        print("yol:", self.filename)
        print(self.filename.find('.docx'))
        print("selffile", self.file_path)
        print("lst", list)
        if self.filename.find('.docx') >= 0:
            print("Docx dosyası")
            doc = bw.Document(self.file_path)
            # pth = self.file_path.split(self.filename)
            # print(doc)
            file_name = self.filename.split('.docx')[0]
            print("dosya ismi", file_name)
            for file in list:
                print("for")
                if file == file_name + ".txt":
                    count = 1

            if count == 1:
                self.message.about(self, "File Uploading", "Bu dosya zaten kayıtlı")
            else:
                # output = pypandoc.convert_file(self.file_path, 'txt', outputfile=path1 + file_name + ".txt")
                # assert output == ""
                # print("out:", output)
                doc.save(path1 + file_name + ".txt")
                self.generalPath = path1 + file_name + ".txt"
                # shutil.copy(pth + file_name + ".txt",path1)
                print("Yeni ad", file_name)
                self.message.about(self, "File Uploding", "Dosya Yüklendi")



        else:
            print("Docx değildir")
            self.path = "C:\\Users\\sulta\\PycharmProjects\\GraphApplication\\Document\\" + self.filename
            self.generalPath = self.path
            shutil.copy(self.file_path, path1)
            self.message.about(self, "File Uploding", "Dosya Yüklendi")
            print("Yeni path", self.path)

        f = open("C:\\Users\\sulta\\PycharmProjects\\GraphApplication\\SaveDirectory\\SaveGeneralPath.txt", 'w')
        f.write(self.generalPath)
        f.close()

    def SFsClicking(self):
        print("Özet Dosyasını Yükle ve kaydet")
        path1 = "C:\\Users\\sulta\\PycharmProjects\\GraphApplication\\SummaryDocument\\"
        count = 0
        list = os.listdir(path1)

        if self.filename.find('.docx'):
            print("Docx dosyası")
            doc = bw.Document(self.file_path)
            file_name = self.filename.split('.docx')[0]
            for file in list:
                if file == file_name + ".txt":
                    count = 1

            if count == 1:
                self.message.about(self, "File Uploading", "Bu dosya zaten kayıtlı")
            else:
                doc.save(path1 + file_name + ".txt")
                self.generalPath = path1 + file_name + ".txt"
                print("Yeni ad", file_name)
                self.message.about(self, "File Uploding", "Dosya Yüklendi")




        else:
            print("Docx değildir")
            self.path = "C:\\Users\\sulta\\PycharmProjects\\GraphApplication\\SummaryDocument\\" + self.filename
            self.generalPath = self.path
            shutil.copy(self.file_path, path1)
            self.message.about(self, "File Uploding", "Dosya Yüklendi")
            print("Yeni path", self.path)

        f = open("C:\\Users\\sulta\\PycharmProjects\\GraphApplication\\SaveDirectory\\SaveSummaryGeneralPath.txt", 'w')
        f.write(self.generalPath)
        f.close()

    # noinspection PyUnresolvedReferences
    def initUi(self):  # Özellikler tanımlandı
        self.lbl_name.setText('Dosya Yolu:')
        self.lbl_name.setFont(QFont('Arial', 20))
        self.lbl_name.move(50, 50)

        self.lbl_path.setText("klasör yolu...")
        self.lbl_path.move(250, 50)
        self.lbl_path.resize(1200, 35)
        self.lbl_path.setFont(QFont('Arial', 20))
        self.lbl_path.setStyleSheet("QLabel { color : red; }")

        self.openFileExplorer.setText("Dosya Gezgini Aç")
        self.openFileExplorer.move(50, 150)
        self.openFileExplorer.setFont(QFont('Arial bold', 15))
        self.openFileExplorer.adjustSize()
        self.openFileExplorer.resize(200, 80)
        self.openFileExplorer.setStyleSheet("background-color: brown;color:white")
        self.openFileExplorer.clicked.connect(self.FeClicking)

        self.saveFile.setText("Metin Dosyasını Yükle")
        self.saveFile.move(300, 150)
        self.saveFile.setFont(QFont('Arial bold', 15))
        self.saveFile.adjustSize()
        self.saveFile.resize(250, 80)
        self.saveFile.setStyleSheet("background-color: brown;color:white")
        self.saveFile.clicked.connect(self.FsClicking)

        self.saveFileSummary.setText("Özet Dosyasını Yükle")
        self.saveFileSummary.move(600, 150)
        self.saveFileSummary.setFont(QFont('Arial bold', 15))
        self.saveFileSummary.adjustSize()
        self.saveFileSummary.resize(250, 80)
        self.saveFileSummary.setStyleSheet("background-color: brown;color:white")
        self.saveFileSummary.clicked.connect(self.SFsClicking)

        self.createGraph.setText("Graf Oluştur")
        self.createGraph.move(350, 270)
        self.createGraph.setFont(QFont('Arial bold', 15))
        self.createGraph.adjustSize()
        self.createGraph.resize(200, 80)
        self.createGraph.setStyleSheet("background-color: black;color:white")
        self.createGraph.clicked.connect(self.Create_Graph)


class SetSummaryPage(QWidget):
    def __init__(self, point, finalS):
        super(SetSummaryPage, self).__init__()
        self.sortedSent = None
        self.englishAbbreviations = ["Dr.", "Mr.", "Mrs.", "Ms.", "Ave.", "Blvd.", "Ln.",
                                     "Rd.", "Asst.", "Corp.", "Inc.", "etc.", "e.g.", "i.e.",
                                     "C.V.", "n.b", "P.S", "et al.", "fig.",
                                     "ft.", "hr.", "min.",
                                     "sq.", "St.", "yd.", "tbs.", "tbsp.", "a.m.", "p.m.", "approx."]
        self.paragraph = ""
        self.Scr = point
        self.Finals = finalS
        self.setGeometry(60, 60, 600, 600)
        self.setWindowTitle('Summary Page')

        self.SentencesDict = dict()
        self.getAllOfThem = dict()
        self.Summary()
        self.summary = QLabel(self)
        self.grid = QGridLayout(self)
        self.rougeText = QLabel(self)
        self.rougeScore = QLabel(self)
        self.ShowSummary()
        self.RgScore = ""
        self.rougeScoreFunction()

    def rougeScoreFunction(self):

        file1 = open("C:\\Users\\sulta\\PycharmProjects\\GraphApplication\\SaveDirectory\\SaveSummaryGeneralPath.txt",
                     'r')
        thisPath = file1.readline()
        file1.close()

        file = open(thisPath, 'r')
        line = file.readlines()

        lines = line[2:len(line) - 1]
        p = ""
        for l in lines:
            if len(l) > 1:
                p = p + l

        ROUGE = Rouge()
        reference = p
        candidate = self.paragraph
        score = ROUGE.get_scores(hyps=candidate, refs=reference)
        print(score)
        print("RougeSkor:", score[0]["rouge-1"]["f"])

        self.RgScore = str(round(score[0]["rouge-1"]["f"], 2))
        self.rougeScore.setText(self.RgScore)
        # converted_dict = dict(ROUGE.get_scores(candidate, reference))
        # print("RougeSkor:", converted_dict[0][0])
        file.close()

    def ShowSummary(self):
        self.setLayout(self.grid)
        self.summary.setText(self.paragraph)
        self.summary.setFont(QFont('Arial bold', 10))
        self.summary.adjustSize()
        self.rougeText.setText("ROUGE SKOR:")
        self.rougeText.setFont(QFont('Arial bold', 15))
        self.rougeText.resize(300, 300)
        self.rougeText.move(10, 500)
        self.rougeText.setStyleSheet('color:red')
        self.rougeScore.setFont(QFont('Arial bold', 15))
        self.rougeScore.resize(300, 300)
        self.rougeScore.move(10, 550)
        self.grid.addWidget(self.summary, 0, 0, 1, 1)
        # self.grid.addWidget(self.rougeText, 0, 0, 2, 1)
        # self.grid.addWidget(self.rougeScore, 0, 0, 3, 1)

    def Summary(self):
        file1 = open("C:\\Users\\sulta\\PycharmProjects\\GraphApplication\\SaveDirectory\\SaveGeneralPath.txt", 'r')
        path = file1.readline()
        file1.close()
        file = open(path, 'r')
        line = file.readlines()
        file.close()
        hlines = []
        allSentences = []
        getTrueSentences = []
        getSpecific = line[2:len(line) - 1]
        textAll = ""
        for j in range(0, len(getSpecific)):
            print("1. for")
            if len(getSpecific[j]) > 1:
                hlines.append(getSpecific[j])

        for g in range(0, len(hlines)):
            print("2. for")
            control = 0
            hold = -1
            for i in hlines[g]:
                if i in string.punctuation:
                    control = 1

            if control == 0:  # baslıktır.
                allSentences.append(hlines[g])
            else:
                textAll = textAll + hlines[g] + " "
        print("Tüm text:", textAll)
        someSentences = re.split(r'(?<=[.?!])', textAll)
        c = 1
        print("Bazı Cümleler", someSentences)
        for s in someSentences:
            allSentences.append(s)
            c += 1

        print("Tüm Cümleler:", allSentences)

        k = 0
        num = 0
        while k < len(allSentences):
            print("w")
            y = 0
            if len(allSentences[k]) > 2:
                print("if")
                num += 1
                for p in self.englishAbbreviations:
                    print("for")
                    if allSentences[k].find(p) >= 0:
                        y = 1

                if y == 1:
                    print(k)
                    new = allSentences[k] + allSentences[k + 1]
                    getTrueSentences.append(new)
                    k += 2
                    print("gk:", k)


                else:
                    getTrueSentences.append(allSentences[k])
                    k += 1
            else:
                k += 1

        print("Cümles:", getTrueSentences)
        print("Uzunluk:", num)

        ids = 1
        for i in range(0, num):
            add = 'Cümle ' + str(ids)
            self.SentencesDict[add] = getTrueSentences[i]
            ids += 1

        idb = 1

        for m in range(0, len(self.Finals)):
            print("forx")
            held = 'Cümle ' + str(idb)
            if self.Finals[m] >= self.Scr:
                print("ifx")
                self.getAllOfThem[held] = self.Finals[m]

            idb += 1

        sortedS = sorted(self.getAllOfThem.items(), key=lambda x: x[1], reverse=True)

        self.sortedSent = dict(sortedS)
        print(self.sortedSent)

        idö = 0
        for a in self.sortedSent:
            if idö == 0:
                self.paragraph = self.paragraph + self.SentencesDict[a] + "\n"
            elif idö % 2 == 0 and idö != 0:
                self.paragraph = self.paragraph + self.SentencesDict[a] + "\n"
            else:
                self.paragraph = self.paragraph + self.SentencesDict[a] + " "

            idö += 1


# noinspection PyArgumentList,PyTypeChecker
class SetGraphWindow(QWidget):

    def __init__(self):
        super(SetGraphWindow, self).__init__()
        self.win3 = None
        self.englishAbbreviations = None
        self.Psentences = []
        self.letter = None
        self.gpath = None
        self.setGeometry(40, 40, 1200, 1200)
        self.setWindowTitle('Graph Page')
        self.thisDict = dict()
        self.source = []
        self.target = []
        self.status = []
        self.ProperNounScores = []
        self.NumericScore = []
        self.getAllSim = []
        self.do_graph()
        self.Cumle_Skor()
        self.NumericSkor()

        self.grid = QGridLayout(self)
        self.similaritySentence = QLabel(self)
        self.similaritySentence.setText('Cümle Benzerliği Thresholdu:')
        self.similaritySentence.setStyleSheet('color:red')
        self.similaritySentence.setFont(QFont('Arial bold', 15))
        self.textbox1 = QLineEdit(self)
        self.sButton = QPushButton(self)
        self.sButton.move(20, 150)
        self.sButton.resize(300, 80)
        self.sButton.setText("Benzerlik Oranı Gönder")
        self.sButton.setFont(QFont('Arial bold', 15))
        self.sButton.setStyleSheet("background-color: black;color:white")
        self.ScoreSentence = QLabel(self)
        self.ScoreSentence.setText("Cümle Skoru Thresholdu:")
        self.ScoreSentence.resize(500, 100)
        self.ScoreSentence.move(10, 250)
        self.ScoreSentence.setStyleSheet('color:red')
        self.ScoreSentence.setFont(QFont('Arial bold', 15))
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(10, 340)
        self.textbox2.resize(325, 25)
        self.btn2 = QPushButton(self)
        self.btn2.setText("Özeti Çıkar")
        self.btn2.move(20, 380)
        self.btn2.resize(300, 80)
        self.btn2.setStyleSheet("background-color: black;color:white")
        self.btn2.setFont(QFont('Arial bold', 15))

        self.setLayout(self.grid)
        self.show()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.grid.addWidget(self.canvas, 0, 3, 9, 9)
        self.grid.addWidget(self.similaritySentence, 0, 0, 1, 2)
        self.grid.addWidget(self.textbox1, 0, 0, 2, 2)
        # self.grid.addWidget(self.sButton, 0, 0, 3, 2)
        # self.grid.addWidget(self.ScoreSentence, 0, 0, 5, 2)
        # self.grid.addWidget(self.textbox2, 0, 0, 6, 2)
        # self.grid.addWidget(self.btn2, 0, 0, 6, 2)
        # grid.addChildLayout(textbox1)

        self.changeDict = dict()
        self.changeInDict()
        self.cosSimilar = []
        # self.cosSimilarity()

        self.ShowGraph()
        self.Action()
        self.P3 = []
        self.P4 = []
        self.P4Function()
        self.P5 = []
        self.P5Function()
        self.FinalScore = []
        self.btn2.clicked.connect(self.GetSummary)

    def GetSummary(self):
        print("Cümleleri tekrar dosyadan oku")
        print("Yeni widget class oluştur")
        print("Özeti oraya bastır")
        print("Özet Çıkarma Fonksiyonu burada kaldın")
        getScore = self.textbox2.text()
        y2 = float(getScore) if getScore else 0
        self.win3 = SetSummaryPage(y2, self.FinalScore)
        self.win3.show()

    def FinalScoreFunction(self):
        print("final girdi")
        print("Özel İsim:", self.ProperNounScores)
        print("Numerik:", self.NumericScore)
        print("P3:", self.P3)
        print("P4:", self.P4)
        print("P5:", self.P5)
        for i in range(0, len(self.P5)):
            sumT = self.ProperNounScores[i] + self.NumericScore[i] + self.P3[i] + self.P4[i] + self.P5[i]
            getF = sumT / 2
            self.FinalScore.append(round(getF, 2))
        print("Cümle Skoru:", self.FinalScore)

    def P5Function(self):
        SentenceWords = list()
        tema = []
        for d in self.changeDict:
            words = word_tokenize(self.changeDict[d])
            SentenceWords.append(words)

        for f in range(0, len(SentenceWords)):
            for k in range(0, len(SentenceWords[f])):
                TF = SentenceWords[f].count(SentenceWords[f][k]) / len(SentenceWords[f])

                count = 0
                for doc in SentenceWords:
                    for word in doc:
                        if word == SentenceWords[f][k]:
                            count += 1
                            break
                total_doc_number = len(SentenceWords)
                DF = total_doc_number / count
                from math import log10
                IDF = log10(DF)

                result = TF * IDF
                print("TFxIDF:", result)
                r = round(result, 2)
                if r == (10 / 100):
                    tema.append(SentenceWords[f][k])

        for d in self.changeDict:
            words = word_tokenize(self.changeDict[d])
            t = 0
            for w in range(0, len(words)):
                for h in range(0, len(tema)):
                    if words[w].lower() == tema[h].lower():
                        t += 1
            s = t / len(words)
            self.P5.append(round(s, 2))
        print("P5:", self.P5)

    def P4Function(self):

        headers = word_tokenize(self.letter)

        print("headers:", headers)
        for g in self.changeDict:
            num = 0
            words = word_tokenize(self.changeDict[g])
            print("words:", words)
            for i in range(0, len(words)):
                for j in range(0, len(headers)):
                    if words[i].lower() == headers[j].lower():
                        num += 1

            sk = num / (len(words))
            self.P4.append(round(sk, 2))

        print("P4:", self.P4)

    def Action(self):
        print("Aksiyon")

        self.sButton.clicked.connect(self.SBClicked)

    def SBClicked(self):
        print("btn1 tıklandı")
        self.figure.clf()
        getSim = self.textbox1.text()
        y1 = float(getSim) if getSim else 0
        print(y1)
        getSentSim = []
        nodeSentence = list()
        print(self.getAllSim)
        print("len:", len(self.changeDict))
        count = 1
        for i in range(0, len(self.source)):
            print("for")
            getSentSim.append(self.getAllSim[i])
            if count % (len(self.thisDict) - 1) == 0:
                print("i:", i)
                print(getSentSim)
                print("if")
                total = 0
                for j in range(0, len(getSentSim)):
                    # print("içfor")
                    # print("sSim", getSentSim[j])
                    if float(getSentSim[j]) >= y1:
                        # print("sonuncu if")
                        total += 1
                print("Say:", total)
                getSentSim = []
                nodeSentence.append(total)
            count += 1
        print(nodeSentence)

        for i in range(0, len(nodeSentence)):
            Skore = nodeSentence[i] / (len(self.changeDict) - 1)
            self.P3.append(round(Skore, 2))
        print("P3:", self.P3)

        self.FinalScoreFunction()

        df = pd.DataFrame({'Source': self.source,
                           'Target': self.target,
                           'Status': self.status
                           })

        # Create graph
        g = nx.from_pandas_edgelist(df, 'Source', "Target", ["Status"], create_using=nx.DiGraph())

        pos = nx.spring_layout(g)
        # print("pos:", pos['Ali'])

        pos_higher = {}
        pos1_higher = {}

        for k, v in pos.items():
            if v[1] > 0:
                pos_higher[k] = (v[0] - 0.1, v[1] + 0.1)
            else:
                pos_higher[k] = (v[0] - 0.1, v[1] - 0.1)
        labels = dict()
        id = 1
        for i in range(0, len(nodeSentence)):
            a = 'Cümle ' + str(id)
            labels[a] = nodeSentence[i]
            id += 1

        for k, v in pos.items():
            if v[1] > 0:
                pos1_higher[k] = (v[0] + 0.1, v[1] - 0.1)
            else:
                pos1_higher[k] = (v[0] + 0.1, v[1] + 0.1)

        labels1 = dict()
        id1 = 1
        for i in range(0, len(self.FinalScore)):
            a = 'Cümle ' + str(id1)
            labels1[a] = self.FinalScore[i]
            id1 += 1

        nx.draw(g, pos, with_labels=True, node_color='red', node_size=3000, font_color='white', font_size=10,
                font_family="Times New Roman", font_weight="bold", width=1)

        nx.draw_networkx_labels(g, pos_higher, labels, bbox=dict(boxstyle="round", color='yellow'))
        nx.draw_networkx_labels(g, pos1_higher, labels1, bbox=dict(boxstyle="round", color='pink'))

        edge_labels = dict([((n1, n2), d['Status'])
                            for n1, n2, d in g.edges(data=True)])

        nx.draw_networkx_edge_labels(g,
                                     pos, edge_labels=edge_labels,
                                     label_pos=0.5,
                                     font_color='white',
                                     bbox=dict(boxstyle="round", color='green'),
                                     font_size=7,
                                     font_weight='bold',
                                     verticalalignment='bottom')
        self.canvas.draw_idle()

        print("Function")

    def do_graph(self):

        lines = None
        str = ""
        file1 = open("C:\\Users\\sulta\\PycharmProjects\\GraphApplication\\SaveDirectory\\SaveGeneralPath.txt", 'r')
        self.gpath = file1.readline()
        file1.close()

        self.englishAbbreviations = ["Dr.", "Mr.", "Mrs.", "Ms.", "Ave.", "Blvd.", "Ln.",
                                     "Rd.", "Asst.", "Corp.", "Inc.", "etc.", "e.g.", "i.e.",
                                     "C.V.", "n.b", "P.S", "et al.", "fig.",
                                     "ft.", "hr.", "min.",
                                     "sq.", "St.", "yd.", "tbs.", "tbsp.", "a.m.", "p.m.", "approx."]
        print("path alinma", self.gpath)
        file = open(self.gpath, 'r')
        line = file.readlines()

        # line = file.readline()
        lns = file.read()
        lines = line[2:len(line) - 1]
        # splines = lns[2:len(line) - 1]
        # print("splines:", lns)
        words = lns.split(" ")
        sent = ""
        control = 0
        sentens1 = []
        wrd = ""
        """for i in range(0, len(lns)):
            wrd += lns[i]
            if lns[i] == ' ':
                wordList.append(wrd)
                wrd = ""

        for j in wordList:
            print("k:", j)"""

        """for w in words:
            control = 0
            if len(w) > 1:
                print("k:", w)
                for j in englishAbbreviations:
                    if w == j:
                        print("v:", w)
                        control = 1
                        break

                if control == 1:
                    get_word: str = ""
                    a = w.split(".")
                    print("splitlenmiş:", a)
                    w = get_word.join(a)
                    sent = sent + w + " "
                else:
                    if w.find(".") >= 0:
                        sent = sent + w + " "
                    else:
                        sent = sent + w + " "

        print("Düzenlenmiş Cümle:", sent)

        sentences = re.split(r'[.!?]+', sent)
        for s in sentences:
            if len(s) > 2:
                print("C:", s)
                if s.find("Evaluation") == -1:
                    # print("Sentences C:", s)
                    sentens1.append(s)
                elif s.__contains__("Created with Aspose") != 1:
                    # print("Sentences C:", s)
                    sentens1.append(s)
                elif s.__contains__("Words") != 1:
                    # print("Sentences C:", s)
                    sentens1.append(s)
                elif s.__contains__("Copyright 2003-2023 Aspose Pty Ltd") != 1:
                    # print("Sentences C:", s)
                    sentens1.append(s)
                elif s.__contains__("Created with an evaluation copy of Aspose") != 1:
                    # print("Sentences C:", s)
                    sentens1.append(s)
                elif s.__contains__("To discover the full versions of our APIs please visit: https://products") != 1:
                    # print("Sentences C:", s)
                    sentens1.append(s)
                elif s.__contains__("aspose") != 1:
                    # print("Sentences C:", s)
                    sentens1.append(s)
                elif s.__contains__("com/words/") != 1:
                    # print("Sentences C:", s)
                    sentens1.append(s)

        for s in sentens1:
            print("YC:", s)"""

        fLines = list()
        sentens = list()
        sentens1 = list()
        trying = "Merhaba.Hoşgeldiniz."
        count = 0
        control = 0
        index = 1

        st = ""
        # print(student['2'])
        for l in lines:
            if len(l) > 1:
                print("l:", l)
                fLines.append(l)

        print("Z:", fLines)

        for e in fLines:
            print(e)
            if len(e) > 1:
                # print(s)
                words = e.split(" ")
                sent = ""
                for w in words:
                    control = 0
                    for j in self.englishAbbreviations:
                        if w == j:
                            print("Kısaltma:", w)
                            control = 1
                            break

                    if control == 1:
                        get_word: str = ""
                        a = w.split(".")

                        w = get_word.join(a)

                        sent = sent + w + " "
                    else:
                        sent = sent + w + " "

                # s = sentc
                print("cümle:", sent)
                sentens.append(sent)

        for s in sentens:
            if count == 1:
                s += "."
            st = st + s + " "
            count += 1
        print("sentens", sentens)
        print("Text:", st)

        # self.Psentences = st.rsplit(r'[.!?]+')

        sentences = re.split(r'[.!?]+', st)
        for s in sentences:
            if len(s) > 3:
                print("C:", s)
                sentens1.append(s)
        print("cümleler:", sentens1)
        for idx, ele in enumerate(sentens1):
            self.thisDict[idx] = ele

        # self.letter = sentens1[0]
        # print("baslik", self.letter)
        for i in self.thisDict:
            print(self.thisDict[i])
        print(len(self.thisDict))

        file.close()
        """for e in sentens:
        
            sentences = re.split(r'[.!?]+', e)
            for s in sentences:
                if len(s) > 2:
                    print("Sentences C:", s)
                    sentens1.append(s)"""

        """for idx, ele in enumerate(sentens1):
            self.thisDict[idx] = ele

        for i in self.thisDict:
            print(self.thisDict[i])"""

    def Cumle_Skor(self):
        print("self.thisDict fonksiyonundan cümleler alınacak,key value ")
        for idx in self.thisDict:
            tagged_sent = pos_tag(self.thisDict[idx].split())
            propernouns = [word for word, pos in tagged_sent if pos == 'NNP']
            print("Özel isimler:", propernouns)
            self.ProperNounScores.append(round(len(propernouns) / len(tagged_sent), 2))
            print("Skor:", round(len(propernouns) / len(tagged_sent), 2))

    def NumericSkor(self):

        for idx in self.thisDict:
            count = 0
            numCount = 0
            getWords = self.thisDict[idx].split(" ")
            for w in getWords:
                num = 0
                if len(w) > 0:
                    count += 1
                for m in w:
                    if m.isdigit():
                        num = 1
                        break

                if num == 1:
                    numCount += 1
            print("Dictionary Words:", getWords)
            print("Uzunluk:", count)
            print("Numeric Skor:", round((numCount / count), 2))
            self.NumericScore.append(round((numCount / count), 2))

    def changeInDict(self):
        say = 1
        for idx in self.thisDict:
            s = ""
            s2 = ""
            ps = PorterStemmer()
            str1 = self.thisDict[idx]
            print(str1)
            # tokenizer = RegexpTokenizer(r"[a-zA-Z0-9]+")
            words1 = word_tokenize(str1)

            words2 = []
            for w in words1:  # Kök bulma
                a = ps.stem(w)
                words2.append(a)

            stop_words = set(stopwords.words('english'))
            filtered_sentence = [w for w in words2 if not w.lower() in stop_words]
            filtered_sentence = []
            for w in words2:
                if w not in stop_words:
                    filtered_sentence.append(w)
            # print(filtered_sentence)

            for f in filtered_sentence:
                s = s + f + " "
            # print(s)

            tokenizer = RegexpTokenizer(r"[a-zA-Z0-9]+")
            # Tokenize str1
            lastWords = tokenizer.tokenize(s)
            for l in lastWords:
                s2 = s2 + l + " "
            self.changeDict['Cümle ' + str(say)] = s2
            say += 1
            print(lastWords)
        self.letter = self.changeDict['Cümle 1']
        print('baslık', self.letter)
        for idp in self.changeDict:
            print(idp, self.changeDict[idp])

    def cosSimilarity(self):

        def cosine(u, v):
            return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

        tokenized_sent = []
        for s in self.changeDict:
            tokenized_sent.append(word_tokenize(self.changeDict[s].lower()))
        print(tokenized_sent)
        tagged_data = [TaggedDocument(d, [i]) for i, d in enumerate(tokenized_sent)]
        model = Doc2Vec(tagged_data, vector_size=15, window=2, min_count=1, epochs=40)
        for h in range(0, len(self.source)):
            s1 = word_tokenize(self.changeDict[self.source[h]].lower())
            s2 = word_tokenize(self.changeDict[self.target[h]].lower())
            s1_test = model.infer_vector(s1)
            s2_test = model.infer_vector(s2)
            sim = cosine(s1_test, s2_test)
            rnd = round(sim, 2)
            print(round(sim, 2))
            self.cosSimilar.append(rnd)

        """for h in range(0, len(self.source)):
            s1 = self.changeDict[self.source[h]]
            s2 = self.changeDict[self.target[h]]
            a1 = self.source[h]
            a2 = self.target[h]

            tokenized_sent = []
            for s in self.changeDict:
                if s != a1:
                    tokenized_sent.append(word_tokenize(self.changeDict[s].lower()))

            print(tokenized_sent)
            tagged1_data = [TaggedDocument(d, [i]) for i, d in enumerate(tokenized_sent)]
            model1 = Doc2Vec(tagged1_data, vector_size=15, window=2, min_count=1, epochs=60)

            test_doc = word_tokenize(s1.lower())
            test_doc_vector = model1.infer_vector(test_doc)

            tokenized1_sent = []
            for s in self.changeDict:
                if s != a2:
                    tokenized1_sent.append(word_tokenize(self.changeDict[s].lower()))

            print(tokenized1_sent)
            tagged2_data = [TaggedDocument(d, [i]) for i, d in enumerate(tokenized1_sent)]
            model2 = Doc2Vec(tagged2_data, vector_size=15, window=2, min_count=1, epochs=60)

            test2_doc = word_tokenize(s2.lower())
            test2_doc_vector = model2.infer_vector(test2_doc)
            # print("t1:", test_doc_vector)
            # print("t2:", test2_doc_vector)
            sim = cosine(test_doc_vector, test2_doc_vector)
            print(round(sim, 2))
            # print(model.dv.most_similar(positive=[test_doc_vector]))"""

        print("cos girdi.")

        # test_doc = word_tokenize("I had pizza and pasta".lower())
        # test_doc_vector = model1.infer_vector(test_doc)
        # model1.docvecs.most_similar(positive=[test_doc_vector])

        """def cosine(u, v):
            return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

        model = SentenceTransformer('bert-base-nli-mean-tokens')

        for k in range(0, len(self.source)):
            print("2. fo")
            query1 = self.changeDict[self.source[k]]
            print(query1)
            query1_vec = model.encode(query1)[0]
            print(query1_vec)
            query2 = self.changeDict[self.target[k]]
            print(query2)
            query2_vec = model.encode(query2)[0]
            print(query2_vec)
            sim = cosine(query1_vec, query2_vec)
            print("Sentence1 = ", query1, "Sentence2 = ", query2, "; similarity = ", sim)"""

        # sentence_embeddings = model.encode(sentences)

    def ShowGraph(self):
        self.figure.clf()

        seed = 0  # Çalıştırdığında sabit olsun diye
        random.seed(seed)
        np.random.seed(seed)

        say = 1
        sentencesLabels = []

        for h in range(0, len(self.changeDict)):
            sentencesLabels.append('Cümle ' + str(say))
            say += 1

        print(sentencesLabels)

        # source = []
        # target = []
        # status = []
        for i in range(0, len(sentencesLabels)):
            for j in range(0, len(sentencesLabels) - 1):
                self.source.append(sentencesLabels[i])
        print("source", self.source)
        k = 0
        start = 0
        end = len(self.source)
        count = 0
        # other = []
        posT = 0
        for i in range(start, end):

            if i % (len(sentencesLabels) - 1) == 0:
                other = []
                for p in range(0, len(sentencesLabels)):
                    if p != count:
                        other.append(sentencesLabels[p])

                for o in other:
                    self.target.append(o)
                count += 1

        # target = ["Veli", "Ahmet", "Ali", "Ahmet", "Ali", "Veli"]
        print("target", self.target)
        print(self.changeDict)

        # Düzenleme Benzerlik Hesaplama
        start = 0
        end = len(self.source)
        getList = list()
        otherList = list()
        for j in range(start, end):

            tempArray = []
            k1 = self.source[j]
            k2 = self.target[j]
            tempArray.append(k1)
            tempArray.append(k2)
            print(tempArray)
            getList.append(tempArray)
            print("list:", getList)

            if j > 0:
                control = 0
                for a in range(0, len(getList) - 1):
                    if getList[j][0] == getList[a][1] and getList[j][1] == getList[a][0]:
                        control = 1

                if control == 1:
                    otherList.append(getList[j])
                else:
                    print("Eşit değildir.")

        print("OtherList:", otherList)

        # Benzerlik Hesaplama Cümleler arası
        def cosine(u, v):
            return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

        tokenized_sent = []
        for s in self.changeDict:
            tokenized_sent.append(word_tokenize(self.changeDict[s].lower()))
        print(tokenized_sent)
        tagged_data = [TaggedDocument(d, [i]) for i, d in enumerate(tokenized_sent)]
        print("tagged data", tagged_data)
        model = Doc2Vec(tagged_data, vector_size=len(tagged_data), window=2, min_count=1, epochs=len(tagged_data) + 42)
        SiM = []
        for h in range(0, len(self.source)):
            # print("for a girdi")
            lbl1 = self.source[h]
            lbl2 = self.target[h]
            var1 = 0
            for oth in range(0, len(otherList)):
                # print("2. for")
                if otherList[oth][0] == lbl1 and otherList[oth][1] == lbl2:
                    # print("if")
                    var1 = 1

            if var1 == 1:
                s1 = word_tokenize(self.changeDict[lbl1].lower())
                s2 = word_tokenize(self.changeDict[lbl2].lower())
                s1_test = model.infer_vector(s1)
                s2_test = model.infer_vector(s2)
                sim = cosine(s1_test, s2_test)
                rnd = round(sim, 2)
                # print(round(sim, 2))
                strGet = '' + str(rnd)
                self.cosSimilar.append(strGet)
                # self.getAllSim.append(rnd)
                SiM.append(rnd)
            else:
                d = ''
                self.cosSimilar.append(d)
                s1 = word_tokenize(self.changeDict[lbl2].lower())
                s2 = word_tokenize(self.changeDict[lbl1].lower())
                s1_test = model.infer_vector(s1)
                s2_test = model.infer_vector(s2)
                sim = cosine(s1_test, s2_test)
                rnd = round(sim, 2)
                getAll = '' + str(rnd)
                # self.getAllSim.append(rnd)
        print(self.cosSimilar)
        for h in range(0, len(self.source)):
            # add = '' + str(self.cosSimilar[h])
            self.status.append(self.cosSimilar[h])

        for f in range(0, len(self.source)):
            a = self.source[f]
            b = self.target[f]
            hold = None
            for o in range(0, len(otherList)):
                if otherList[o][0] == a and otherList[o][1] == b:
                    hold = o
                    # print("Burada kaldın.")
                else:
                    for k in range(0, len(otherList)):
                        if otherList[k][1] == a and otherList[k][0] == b:
                            hold = k

            self.getAllSim.append(SiM[hold])
        print("Tüm benzerlikler:", self.getAllSim)
        df = pd.DataFrame({'Source': self.source,
                           'Target': self.target,
                           'Status': self.status
                           })

        # Create graph
        g = nx.from_pandas_edgelist(df, 'Source', "Target", ["Status"], create_using=nx.DiGraph())

        pos = nx.spring_layout(g)
        # print("pos:", pos['Ali'])
        nx.draw(g, pos, with_labels=True, node_color='red', node_size=3000, font_color='white', font_size=10,
                font_family="Times New Roman", font_weight="bold", width=1)

        edge_labels = dict([((n1, n2), d['Status'])
                            for n1, n2, d in g.edges(data=True)])

        nx.draw_networkx_edge_labels(g,
                                     pos, edge_labels=edge_labels,
                                     label_pos=0.5,
                                     font_color='white',
                                     bbox=dict(boxstyle="round", color='green'),
                                     font_size=7,
                                     font_weight='bold',
                                     verticalalignment='bottom')
        self.canvas.draw_idle()


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


window()
