@echo off
echo ===============================
echo Installing Requirements (Safe Mode)
echo ===============================

set PIP_NO_PROXY=*

python -m pip install --upgrade pip

python -m pip install pandas --trusted-host pypi.org --trusted-host files.pythonhosted.org
python -m pip install scikit-learn --trusted-host pypi.org --trusted-host files.pythonhosted.org
python -m pip install streamlit --trusted-host pypi.org --trusted-host files.pythonhosted.org
python -m pip install scapy --trusted-host pypi.org --trusted-host files.pythonhosted.org

echo ===============================
echo Done
echo ===============================
pause
