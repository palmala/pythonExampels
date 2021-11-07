import string
import json

if __name__ == "__main__":
    simple_json = '{ "person": {"firstname": "John", "lastname": "Doe"}, "friends": [{' \
                  '"person": {"firstname": "Jane", "lastname": "Doe"}' \
                  '}]}'
    print(simple_json)
    parsed_json = json.loads(simple_json)
    print(parsed_json)
