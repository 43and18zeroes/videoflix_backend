REM "./scripts/up.bat" comment
pip freeze > requirements.txt
git add .
git commit -m "%*"
git push