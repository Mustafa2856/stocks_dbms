## on linux:
'''
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
export FLASK_ENV=development
'''

## dbms setup:
#### install postgresql,libpq-dev
'''
psql postgres
create database stocks_dbms;
'''
'''
export DATABASE_URL=postgresql+psycopg2:///stocks_dbms
'''
