from PyQt4 import QtGui, QtCore


class Window(QtGui.QWidget):
    def __init__(self, rows, columns):
        QtGui.QWidget.__init__(self)
        self.table = QtGui.QTableWidget(self)
        self.table.setRowCount(rows)
        self.table.setColumnCount(columns)
        for column in range(columns):
            for row in range(rows):
                item = QtGui.QTableWidgetItem('Text%d' % row)
                self.table.setItem(row, column, item)
        self.edit = QtGui.QLineEdit(self)
        self.button = QtGui.QPushButton('Search', self)
        self.button.clicked.connect(self.handleButton)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)

    def handleButton(self):
        items = self.table.findItems(
            self.edit.text(), QtCore.Qt.MatchContains)
        if items:
            for item in items:
                print item.row()
                for i in range(6):
                    self.table.setRowHidden(i,True)
                self.table.setRowHidden(item.row(),False)
        else:
            results = 'Found Nothing'
            QtGui.QMessageBox.information(self, 'Search Results', results)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window(6, 3)
    window.resize(350, 300)
    window.show()
    sys.exit(app.exec_())