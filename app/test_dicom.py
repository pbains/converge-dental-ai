import os
import pytest
from dicom import get_dicom_fields, split_dicom_fields

def test_get_dicom_fields_local_file():
    # Use the provided local DICOM file
    dicom_path = os.path.join(os.path.dirname(__file__), "test.dcm")
    fields = get_dicom_fields(dicom_path)
    assert isinstance(fields, dict)
    # Check for some common DICOM fields (may vary based on your test.dcm)
    assert "Error" not in fields
    assert len(fields) > 0

def test_split_dicom_fields():
    # Create a sample fields dict with binary and non-binary values
    fields = {
        "PatientName": "Test Name",
        "PatientID": "12345",
        "PixelData": b"\x00\x01\x02\x03",  # binary field
        "SomeInt": 42,
        "SomeList": [1, 2, 3]
    }
    non_binary, binary = split_dicom_fields(fields)
    assert "PatientName" in non_binary
    assert "PatientID" in non_binary
    assert "SomeInt" in non_binary
    assert "SomeList" in non_binary
    assert "PixelData" in binary
    assert isinstance(non_binary, dict)
    assert isinstance(binary, dict)
    assert len(non_binary) == 4
    assert len(binary) == 1