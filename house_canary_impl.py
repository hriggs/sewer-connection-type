'''Service responsible for getting the property sewer connection type from the House Canary API.'''

import logging
from flask import json, jsonify
import requests

def get_sewer_connection_type_canary_impl(address, zipcode, config_data):
    '''Returns the property sewer connection type from the House Canary API.
    @param address: property address.
    @param zipcode: property zip code.
    @param config_data: configuration data for the API.
    @return the sewer connection type.
    @exception Exception: error occurred when fetching the sewer connection type.'''

    base_url = config_data["base_url"]
    full_url = f"{base_url}/property/details?address={address}&zipcode={zipcode}"

    response = requests.get(full_url)
    if response.status_code != 200:
        logging.error(response.text)
        raise Exception("Error fetching the sewer connection type.")

    sewer_conn_type = json.loads(response.text)["property/details"]["result"]["property"]["sewer"]
    return jsonify({"sewer": sewer_conn_type})
