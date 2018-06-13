PYTHONPATH='./webapp' FLASK_APP=webapp/webapp/app.py flask users create --password password -a testuser@example.com
PYTHONPATH='./webapp' FLASK_APP=webapp/webapp/app.py flask roles create test_hmis_service_stays
PYTHONPATH='./webapp' FLASK_APP=webapp/webapp/app.py flask roles create test_jail_bookings
PYTHONPATH='./webapp' FLASK_APP=webapp/webapp/app.py flask roles add testuser@example.com test_hmis_service_stays
PYTHONPATH='./webapp' FLASK_APP=webapp/webapp/app.py flask roles add testuser@example.com test_jail_bookings

PYTHONPATH='./webapp' FLASK_APP=webapp/webapp/app.py flask users create --password password -a countyone@example.com
PYTHONPATH='./webapp' FLASK_APP=webapp/webapp/app.py flask roles create countyone_hmis
PYTHONPATH='./webapp' FLASK_APP=webapp/webapp/app.py flask roles add countyone@example.com countyone_hmis

PYTHONPATH='./webapp' FLASK_APP=webapp/webapp/app.py flask users create --password password -a countytwo@example.com
PYTHONPATH='./webapp' FLASK_APP=webapp/webapp/app.py flask roles create countytwo_hmis
PYTHONPATH='./webapp' FLASK_APP=webapp/webapp/app.py flask roles add countytwo@example.com countytwo_hmis
