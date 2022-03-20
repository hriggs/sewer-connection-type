install:
	pip install --upgrade pip && pip install -r requirements.txt

lint:
	pylint app.py house_canary_impl.py sample_second_impl.py test_app.py

test:
	pytest test_app.py
