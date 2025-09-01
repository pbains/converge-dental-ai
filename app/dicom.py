import pydicom

def get_dicom_fields(filepath):
    try:
        ds = pydicom.dcmread(filepath)
        fields = {}
        for elem in ds:
            if elem.keyword:
                value = elem.value
                fields[elem.keyword] = value
        return fields
    except Exception as e:
        return {"Error": str(e)}      
    
def split_dicom_fields(fields):
    non_binary = {}
    binary = []
    for key, value in fields.items():
        if isinstance(value, (str, int, float, list, tuple, dict)):
            non_binary[key] = value
        else:
            binary.append(key)
    return non_binary, binary
