
# Запуск API  

Для запуска необходмо установить зависимости  
python -m venv venv  
source venv/bin/activate
pip install -r requirements.txt  
Для загрузки данных необходимо загрузить данные из фикстуры  
python manage.py migrate  
python manage.py loaddata fixtures/data.json  
Для запуска необходимо запустить команду  
python manage.py runserver  
Документация доступна по адресу /swagger/
