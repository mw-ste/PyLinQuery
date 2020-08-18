@echo off

cd %~dp0

echo -- Building python wheel
python setup.py bdist_wheel >nul
copy dist\pylinquery-*-py3-none-any.whl . >nul

echo -- Cleaning up build artifacts...
rmdir /Q /S .\build
rmdir /Q /S .\dist
rmdir /Q /S .\pylinquery.egg-info

echo -- Installing wheel...
for /r %%a in (pylinquery-*-py3-none-any.whl) do (
    pip install --upgrade "%%a" )

pause