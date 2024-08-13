# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 08:18:48 2024

@author: ivanp
"""
import sys
import os
import time

from typing import List
import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import Qt  # pylint: disable=E0611
# the above is false positive - see https://stackoverflow.com/questions/56726580/no-name-qapplication-in-module-pyqt5-qtwidgets-error-in-pylint
import citationtool as ct


class FetchDOIApp(qtw.QMainWindow):
    """
    Simple fetcher qt Window
    """

    def __init__(self):
        super().__init__()
        self.lref_dict = dict()  # {file : {"[LR...]":[doi,doi]}}
        self.doi_dict = dict()  # doi : citation
        self._cit_intext = dict()  # citation : intext
        self.file_paths = list()  # files

        self.init_UI()

    def init_UI(self):  # pylint: disable=C0103
        "Intializes user interface"
        # Create main layout
        layout = qtw.QVBoxLayout()

        # Create QLabel for status messages
        self.statusLabel = qtw.QLabel('Select files to process...', self)  # pylint: disable=C0103
        self.statusLabel.setWordWrap(True)  # Allows text to wrap in QLabel

        # Create QScrollArea and configure
        self.scrollArea = qtw.QScrollArea(self)  # pylint: disable=C0103
        self.scrollArea.setWidgetResizable(True)  # Make the widget inside scrollArea resizable
        self.scrollArea.setFrameShape(qtw.QFrame.NoFrame)  # Remove border

        # Create container widget for QLabel
        self.statusContainer = qtw.QWidget()  # pylint: disable=C0103
        status_layout = qtw.QVBoxLayout()
        status_layout.addWidget(self.statusLabel)
        self.statusContainer.setLayout(status_layout)

        # Set container widget for the scroll area
        self.scrollArea.setWidget(self.statusContainer)

        # Create QProgressBar and configure
        self.progressBar = qtw.QProgressBar(self)  # pylint: disable=C0103
        self.progressBar.setAlignment(Qt.AlignCenter)

        # Add widgets to the main layout
        layout.addWidget(self.scrollArea)  # Expandable area for text
        layout.addWidget(self.progressBar)  # Positioned at the bottom

        # Create a central widget for the main window
        centralWidget = qtw.QWidget()  # pylint: disable=C0103
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        # Configure the main window
        self.setWindowTitle('DOI Processor')
        self.setGeometry(100, 100, 400, 300)
        self.show()

        # Call the method to process files
        self.process_files()

    def process_files(self):
        """
        Handle opening files
        """
        # Open file dialog to select files
        file_dialog = qtw.QFileDialog(self)
        file_dialog.setFileMode(qtw.QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Word Documents (*.docx)")
        file_dialog.setAcceptMode(qtw.QFileDialog.AcceptOpen)
        file_dialog.setOption(qtw.QFileDialog.DontUseNativeDialog, True)
        if file_dialog.exec_():
            self.file_paths = file_dialog.selectedFiles()
        self.extract_and_fetch_dois()
        """
        if file_dialog.exec_():
            self.file_paths = file_dialog.selectedFiles()

        else:
            self.end_session()
        self.extract_and_fetch_dois()
        """

    def end_session(self):
        " End if nothing is selected"
        # Close the main window and quit the application
        self.close()
        qtw.QApplication.quit()
        sys.exit(0)

    def extract_and_fetch_dois(self):
        "fetching dois from the DOCX"

        # Initialize progress bar
        total_files = len(self.file_paths)
        if total_files == 0:
            self.end_session()

        self.progressBar.setMaximum(total_files)
        self.progressBar.setValue(0)

        all_dois = []
        for idx, file_path in enumerate(self.file_paths):
            reference_dict = ct.extract_references(file_path)
            self.lref_dict[file_path] = reference_dict
            all_dois.extend(ct.merge_dois(reference_dict))
            self.progressBar.setValue(idx+1)
        all_dois = list(set(all_dois))
        _text = f"Extracted all DOIs - total of {len(all_dois)} DOIS"
        self.statusLabel.setText(_text)
        # Remove duplicates
        self.fetch_dois(list(set(all_dois)))

    def fetch_dois(self, all_dois: List[str]):
        """
        Fetches DOIs and updates the status label and progress bar.
        This is the time consuming part
        """

        time.sleep(0.5)
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(len(all_dois))
        # Fetch DOIs
        doi_dictionary = dict()
        previous_citation = "-1"
        for idx, ids in enumerate(all_dois):

            try:
                next_doi = f"\n..Fetching doi {all_dois[idx+1]}"
            except IndexError:
                next_doi = ""

            if previous_citation == "-1":
                valid_previous_doi = ""
            else:
                if previous_citation is None:
                    valid_previous_doi = "\nDOI was invalid"
                else:
                    valid_previous_doi = "\n" + previous_citation

            self.statusLabel.setText(f"Fetched doi {ids}\n{valid_previous_doi}{next_doi}")
            previous_citation = ct.fetch_request(ct.CN_BASE_URL + "/" + ids.strip())
            doi_dictionary[ids] = previous_citation
            time.sleep(0.004)
            self.progressBar.setValue(idx + 1)  # Update progress bar
            qtw.QApplication.processEvents()  # Process events to keep GUI responsive

        # Update status label with completion message
        self.statusLabel.setText('Done fetching DOIs!')
        self.progressBar.setValue(len(all_dois))  # Ensure progress bar reaches 100%
        time.sleep(1)
        self.doi_dict = doi_dictionary

        self.end_and_replace()

    def end_and_replace(self):
        """
        Ends the operation
        """
        self.statusLabel.setText("Replacing literature..")
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(len(self.lref_dict))
        # time.sleep(5)

        _end_literature = sorted(list({v for v in self.doi_dict.values() if v is not None}))
        _lit_loc = ct.save_literature_to_docx(_end_literature, self.file_paths[-1])
        self.statusLabel.setText(f'Saved literature to <font color = "green">{_lit_loc}</font>')
        qtw.QApplication.processEvents()  # Process events to keep GUI responsive

        time.sleep(5)

        # Now from doi dict which is DOI citation I want to create citation_intext
        self._cit_intext = {k: ct.intext_cit(v)
                            for k, v in self.doi_dict.items() if v is not None}

        # {file : {"[LR...]":[doi,doi]}}
        good_replacer = dict()
        bad_replacer = dict()
        bad_sentences = ""
        display_text = ""
        idx = 0
        for file, wtdict in self.lref_dict.items():
            good, bad = ct.generate_replacer(wtdict, self._cit_intext)
            good_replacer[file] = good
            bad_replacer[file] = bad

            file_name = os.path.basename(file)
            result_name = ct.add_suffix(file, "_proc")

            ct.save_document(file, result_name, good)

            idx = idx + 1
            self.progressBar.setValue(idx + 1)  # Update progress bar
            display_text = display_text + f'Replaced {len(good)} citation(s) in <font color="green">{file_name}</font> - {len(bad)} was/were bad<br>'
            self.statusLabel.setText(display_text)

            qtw.QApplication.processEvents()  # Process events to keep GUI responsive

            _bad_sentences = [f"\t{x}" for x in ct.recognize_bad_dois(file, list(bad.keys()))]

            bad_sentences = bad_sentences + f'<font color="green">{file_name}</font><br>---<br>' + "\n".join(_bad_sentences) + "<br><br>"

            # time.sleep(2)

        self.statusLabel.setText(bad_sentences)


def run_application():
    "running application"
    app = qtw.QApplication(sys.argv)
    window = FetchDOIApp()  # pylint: disable=W0612
    # app.exec_()
    sys.exit(app.exec_())
