import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QInputDialog, QPushButton, QVBoxLayout, QWidget,
                             QLabel, QGridLayout, QLineEdit, QSpinBox, QGroupBox, QHBoxLayout, QMessageBox)

from create_multiplex import main as create_multiplex

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('DAB+ Multiplex Manager')

        layout = QVBoxLayout()

        self.radio_stations_groupbox = QGroupBox("Stations de radio")
        self.radio_stations_layout = QGridLayout()

        for i in range(len(create_multiplex.radio_stations)):
            self.add_radio_row(i)

        self.radio_stations_groupbox.setLayout(self.radio_stations_layout)
        layout.addWidget(self.radio_stations_groupbox)

        self.add_station_button = QPushButton('Ajouter une station')
        self.add_station_button.clicked.connect(self.add_radio)
        layout.addWidget(self.add_station_button)

        self.start_button = QPushButton('Démarrer le multiplex')
        self.start_button.clicked.connect(self.start_multiplex)
        layout.addWidget(self.start_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_radio_row(self, index):
        station = create_multiplex.radio_stations[index]

        name_label = QLabel(f"Radio {index + 1}:")
        name_edit = QLineEdit(station['name'])
        name_edit.editingFinished.connect(lambda: self.update_radio_name(index, name_edit))
        self.radio_stations_layout.addWidget(name_label, index, 0)
        self.radio_stations_layout.addWidget(name_edit, index, 1)

        bitrate_label = QLabel("Débit binaire:")
        bitrate_spinbox = QSpinBox()
        bitrate_spinbox.setRange(8, 192)
        bitrate_spinbox.setValue(station['bitrate'])
        bitrate_spinbox.valueChanged.connect(lambda value: self.update_radio_bitrate(index, value))
        self.radio_stations_layout.addWidget(bitrate_label, index, 2)
        self.radio_stations_layout.addWidget(bitrate_spinbox, index, 3)

        file_button = QPushButton('Sélectionner le fichier audio')
        file_button.clicked.connect(lambda: self.configure_radio_file(index))
        self.radio_stations_layout.addWidget(file_button, index, 4)

        remove_button = QPushButton('Supprimer')
        remove_button.clicked.connect(lambda: self.remove_radio(index))
        self.radio_stations_layout.addWidget(remove_button, index, 5)

    def update_radio_name(self, index, name_edit):
        create_multiplex.radio_stations[index]['name'] = name_edit.text()

    def update_radio_bitrate(self, index, value):
        create_multiplex.radio_stations[index]['bitrate'] = value

    def configure_radio_file(self, index):
        file_name, _ = QFileDialog.getOpenFileName(self, f'Sélectionner le fichier audio pour Radio {index + 1}', '', 'Audio Files (*.wav)')
        if file_name:
            create_multiplex.radio_stations[index]['input'] = file_name

    def add_radio(self):
        new_station = {
            'name': f'Radio{len(create_multiplex.radio_stations) + 1}',
            'input': '',
            'bitrate': 64
        }
        create_multiplex.radio_stations.append(new_station)
        self.add_radio_row(len(create_multiplex.radio_stations) - 1)

def remove_radio(self, index):
    if len(create_multiplex.radio_stations) > 1:
        create_multiplex.radio_stations.pop(index)

        # Mettre à jour l'affichage
        for i in reversed(range(self.radio_stations_layout.count())):
            self.radio_stations_layout.itemAt(i).widget().setParent(None)
        for i in range(len(create_multiplex.radio_stations)):
            self.add_radio_row(i)
    else:
        QMessageBox.warning(self, "Suppression de station", "Au moins une station doit être présente dans le multiplex.")

def start_multiplex(self):
    for station in create_multiplex.radio_stations:
        if not station['input']:
            QMessageBox.warning(self, "Fichier audio manquant", f"Veuillez sélectionner un fichier audio pour {station['name']}.")
            return

    create_multiplex() if name == 'main':
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())


