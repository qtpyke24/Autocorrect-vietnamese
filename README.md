# Autocorrect-vietnamese

pip install -r requirements.txt

python autocorrect.py

.exe extract:
pyinstaller --onefile --add-data "vi_VN.dic;." --add-data "vi_VN.aff;." autocorrect.py
