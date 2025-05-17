REM "./scripts/up.bat" commitname
pip freeze > requirements.txt
git add .
git commit -m "%*"
git push
ssh christoph@34.40.26.126 "cd /home/c_wagner_germany/projects/videoflix_backend && git pull && sudo supervisorctl restart videoflix_gunicorn && sudo systemctl restart supervisor"