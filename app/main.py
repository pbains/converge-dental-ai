
# Main GUI for DICOM processing and polygon drawing

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLineEdit, QLabel, QHBoxLayout
)
from preprocess import preprocess_dicom
from polygon import draw_polygon
import boto3
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DICOM Polygon Drawer")
        layout = QVBoxLayout()

        # Local file selection
        self.file_label = QLabel("Selected file: None")
        self.file_btn = QPushButton("Select Local File")
        self.file_btn.clicked.connect(self.select_local_file)

        # S3 file selection
        s3_layout = QHBoxLayout()
        self.s3_bucket = QLineEdit()
        self.s3_bucket.setPlaceholderText("S3 Bucket")
        self.s3_key = QLineEdit()
        self.s3_key.setPlaceholderText("S3 Key")
        self.s3_btn = QPushButton("Download from S3")
        self.s3_btn.clicked.connect(self.download_s3_file)
        s3_layout.addWidget(self.s3_bucket)
        s3_layout.addWidget(self.s3_key)
        s3_layout.addWidget(self.s3_btn)

        # Processing buttons
        self.preprocess_btn = QPushButton("Preprocess DICOM")
        self.preprocess_btn.clicked.connect(self.preprocess)
        self.polygon_btn = QPushButton("Draw Polygon")
        self.polygon_btn.clicked.connect(self.draw_polygon)

        layout.addWidget(self.file_label)
        layout.addWidget(self.file_btn)
        layout.addLayout(s3_layout)
        layout.addWidget(self.preprocess_btn)
        layout.addWidget(self.polygon_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.selected_file = None

    def select_local_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select DICOM File")
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(f"Selected file: {file_path}")

    def download_s3_file(self):
        bucket = self.s3_bucket.text().strip()
        key = self.s3_key.text().strip()
        if bucket and key:
            s3 = boto3.client('s3')
            local_path = os.path.join(os.getcwd(), key.split('/')[-1])
            try:
                s3.download_file(bucket, key, local_path)
                self.selected_file = local_path
                self.file_label.setText(f"Downloaded S3 file: {local_path}")
            except Exception as e:
                self.file_label.setText(f"S3 download error: {e}")

    def preprocess(self):
        if self.selected_file:
            preprocess_dicom(self.selected_file)
        else:
            self.file_label.setText("No file selected.")

    def draw_polygon(self):
        if self.selected_file:
            draw_polygon(self.selected_file)
        else:
            self.file_label.setText("No file selected.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
