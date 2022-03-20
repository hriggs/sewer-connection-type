'''Tests for app.py. Make sure to run `flask run` prior to testing.'''

import requests

def test_get_sewer_connection_type_success():
    ''' Tests that the get sewer connection type API works as expected
    when called with all the required parameters and with a bearer token.'''

    headers = {'Authorization' : 'Bearer SOME-TOKEN'}
    response = requests.get(
        "http://127.0.0.1:5000/sewer-connection-type?address=123+Main+St&zipcode=94132",
        headers=headers
        )
    assert response.status_code == 200
    assert response.text == "{\"sewer\":\"septic\"}\n"

def test_get_sewer_connection_type_missing_address_and_zipcode():
    ''' Tests that the get sewer connection type API returns an error
    when the address and zipcode are misssing.'''

    headers = {'Authorization' : 'Bearer SOME-TOKEN'}
    response = requests.get("http://127.0.0.1:5000/sewer-connection-type", headers=headers)
    assert response.status_code == 400
    assert response.text == "Missing parameters: address, zipcode"

def test_get_sewer_connection_type_missing_address():
    ''' Tests that the get sewer connection type API returns an error
    when the address is misssing.'''

    headers = {'Authorization' : 'Bearer SOME-TOKEN'}
    response = requests.get(
        "http://127.0.0.1:5000/sewer-connection-type?zipcode=94132",
        headers=headers
        )
    assert response.status_code == 400
    assert response.text == "Missing parameters: address"

def test_get_sewer_connection_type_missing_zipcode():
    ''' Tests that the get sewer connection type API returns an error
    when the zipcode is misssing.'''

    headers = {'Authorization' : 'Bearer SOME-TOKEN'}
    response = requests.get(
        "http://127.0.0.1:5000/sewer-connection-type?address=123+Main+St",
        headers=headers
        )
    assert response.status_code == 400
    assert response.text == "Missing parameters: zipcode"

def test_get_sewer_connection_type_missing_auth_token():
    ''' Tests that the get sewer connection type API returns an error
    when the authorization bearer token is misssing.'''

    response = requests.get(
        "http://127.0.0.1:5000/sewer-connection-type?address=123+Main+St&zipcode=94132"
        )
    assert response.status_code == 401
    assert response.text == '<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\">\n'\
    '<title>401 Unauthorized</title>\n'\
    '<h1>Unauthorized</h1>\n'\
    '<p>The server could not verify that you are authorized to access the URL requested. '\
    'You either supplied the wrong credentials (e.g. a bad password), '\
    'or your browser doesn&#x27;t understand how to supply the credentials required.</p>\n'
