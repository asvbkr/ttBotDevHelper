echo Make localization
cd BotFileToAudio
..\venv\Scripts\python ../manage.py makemessages -l ru
..\venv\Scripts\python ../manage.py makemessages -l en
..\venv\Scripts\python ../manage.py compilemessages
cd ..