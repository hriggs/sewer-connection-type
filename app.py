'''Service responsible for fetching the property sewer connection type.
Delegates to the correct external API based on the service configuration.'''

import logging
from functools import wraps
from flask import abort, Flask, json, request, Response
from house_canary_impl import get_sewer_connection_type_canary_impl
from sample_second_impl import get_sewer_connection_type_second_impl

app = Flask(__name__)

def get_sewer_connection_type(address, zipcode):
    '''Returns the property sewer connection type from the API specified in the config
    and delegates it to the correct service.
    @param address: property address.
    @param zipcode: property zip code.
    @return the sewer connection type.
    @exception NotImplementedError: the API in the config has not been implemented.
    @exception error opening config file.
    '''

    with open('config.json', encoding="utf8") as config_file:
        config_data = json.load(config_file)
        api = config_data["api"]
        match api:
            case "house-canary":
                return get_sewer_connection_type_canary_impl(address, zipcode, config_data)
            case "sample-second-impl":
                return get_sewer_connection_type_second_impl(address, zipcode, config_data)
            case _:
                raise NotImplementedError("API '{api}' not implemented.")

def create_validation_message_str(parameters):
    '''Creates a validation message based on the given list of parameters.
    @param parameters: a list of '(string, <string|None>)' tuples where
    the first item is the parameter name and the second item is the parameter value.
    '''

    validation_msg = ""
    for parameter in parameters:
        if not parameter[1]:
            if validation_msg == "":
                validation_msg = f"Missing parameters: {parameter[0]}"
            else:
                validation_msg += f", {parameter[0]}"

    return validation_msg

def authorize(func):
    '''Validates the authorization details.
    This should have much more robust checks than is shown here.'''
    @wraps(func)
    def decorated_function(*args, **kws):
        if not 'Authorization' in request.headers:
            abort(401)
        # more auth checks would go here
        return func(*args, **kws)
    return decorated_function

@app.route('/sewer-connection-type', methods=['GET'])
@authorize
def get_sewer_connection_type_route():
    '''Returns the property sewer connections type for the property with 'address' and 'zipcode'.'''

    address = request.args.get('address')
    zipcode = request.args.get('zipcode')

    validation_msg = create_validation_message_str([("address", address), ("zipcode", zipcode)])
    if validation_msg != "":
        return Response(validation_msg, status=400)

    try:
        return get_sewer_connection_type(address, zipcode)
    # pylint: disable=broad-except
    except Exception as exception:
        logging.error(exception)
        return Response(str(exception), status=400)
