# Main GUI for DICOM processing and polygon drawing

from preprocess import preprocess_dicom
from polygon import draw_polygon
import boto3
import os
from flask import Flask, render_template, request
from dicom import get_dicom_fields, split_dicom_fields  # Now imported from dicom.py

app = Flask(__name__)

def list_s3_files(bucket):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket)
    return [obj['Key'] for obj in response.get('Contents', [])]

@app.route('/', methods=['GET', 'POST'])
def upload_and_list():
    files = []
    dicom_fields = None
    binary_fields = None
    bucket = request.args.get('bucket', 'your-default-bucket')
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            filename = uploaded_file.filename
            upload_path = os.path.join('uploads', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            uploaded_file.save(upload_path)
            fields = get_dicom_fields(upload_path)
            dicom_fields, binary_fields = split_dicom_fields(fields)
    try:
        files = list_s3_files(bucket)
    except Exception:
        files = ['Could not list files. Check AWS credentials and bucket name.']
    return render_template('upload.html', files=files, dicom_fields=dicom_fields, binary_fields=binary_fields)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)
