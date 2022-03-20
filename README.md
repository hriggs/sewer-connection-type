# Property Sewer Connection Type Service

This is a simple service that fetches and returns the property sewer connection type from the API specified in the configuration file (`config.json`).

Uses a [SwaggerHub mock API](https://app.swaggerhub.com/apis-docs/api-tests8/house-canary-mock-api/1.0.0).

## Installation

The Makefile will install the needed dependencies. 

```bash
make install
```

Start the service using Flask. 

```bash
flask run
```

## Usage

### Request

The service currently supports the following request:

- Verb: `GET`
- Base URL: `http://127.0.0.1:5000`
- Path: `/sewer-connection-type`
- Query Parameters:
    - `address` (required)
    - `zipcode` (required)
- Headers:
    - `Authorization: Bearer <TOKEN>`

Example:

```bash
curl "http://127.0.0.1:5000/sewer-connection-type?address=123+Main+St&zipcode=94132" -H "Authorization: Bearer AbCdEf123456"
```

*NOTE:* The token can be a random collection of characters; no authorization is actually happening.

### Response

The response is a JSON object where the only key is `sewer` and the value is the sewer connection type. 

Example:

```json
{
    "sewer" : "septic"
}
```

### Lint

Lint the `.py` files via the Makefile. 

```bash
make lint
```

### Test

Run the tests via the Makefile. Note that `flask run` must be called prior to running the tests.

```bash
make test
```

## Design Considerations and Next Steps

### The Framework

This service uses Flask. I initially planned to use Django as the framework, but that seemed too heavyweight for this service. I have never used Flask or Django before though, so it is possible that I misunderstood the intended usage of these frameworks.

### Reusability

The initial purpose of this service was simply to determine if the property sewer connection type was "septic" or not. Rather than returning a boolean, the service is returning the sewer connection type and it will be up to the caller to use that information as they see fit. This way, the same service and API can be used in different ways by different callers. 

### Scalability and Maintainability

The requirements say that "over time, we may find other third parties with this info, or this particular third party may change their API, and we want to leave the web app implementation alone." 

To address this, the service uses the [facade pattern](https://en.wikipedia.org/wiki/Facade_pattern): the API endpoint calls a function that then delegates the service logic based on the service's configuration. This way, the actual functionality is abstracted away from the caller and it is easy to swap out different implementations by changing the config and adding new implementation files or packages. See the `sample_second_impl.py` file as an example of another (Hello World-like) service that could be swapped in if the config file is changed.

In a more robust, production-ready service, the different implementations would likely each be in their own packages and include better configuration management. For example, each implementation package could have its own configuration file and some global configuration could point to that configuration, rather than having one global `config.json` file with implementation-specific details. 

I also considered creating an interface or abstract class that each API implementation would implement and using a separate [factory](https://en.wikipedia.org/wiki/Factory_method_pattern) that would create the correct implementation object based on the config. Then, the app could just call the same implementation method on the returned class, rather than using the switch statement seen in `get_sewer_connection_type()`.

Finally, I wasn't sure if it was safe to assume all APIs would only require an address and zipcode (I did assume the information might be sent differently to different APIs). If they might need other information, then we could easily add another query parameter and that would not affect the other implementations. However, this would involve updating `get_sewer_connection_type()` to accept another parameter. To address this, we could have that function accept a HashMap where the key is the query parameter name and the value is the value provided by the caller. Relatedly, this made me consider if the query parameter validation should belong to the external API implementations instead. However, I assumed that all external APIs would require the address and zipcode at the very least, so that validation seemed fair to add to the endpoint function itself.

There would also need to be better dependency vendoring and test coverage. 

However, in the spirit of [KISS](https://en.wikipedia.org/wiki/KISS_principle) and [YAGNI](https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it), I kept the service as simple as possible to fulfill the current needs and not overengineer the solution. All these design decisions are things I would discuss with the team before implementing.

### Security

For this service to be used in production, it would need to have much tighter access control. Currently, the service simply checks that the string "Authorization" is in the request header, but does not perform any checks on the actual bearer token (this is obviously not enough). There would also need to be some support for sending the correct credentials to the external API that the service is calling. These would be different credentials than are needed to access this service, so we would need to implement some type of credential/token exchange, so that the correct external API could be called. 

Although this service is not currently accessing extremely sensitive details, such as credit card details or health data, it is still important that the service authenticates the caller to protect against DoS (and likely other) attacks. Additionally, we may want to use this service to call other APIs that include more sensitive data in the future.
