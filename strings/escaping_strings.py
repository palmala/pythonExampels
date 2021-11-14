import json

if __name__ == "__main__":
    simple_json = '{ "person": {"firstname": "John", "lastname": "Doe"}, "friends": [{' \
                  '"person": {"firstname": "Jane", "lastname": "Doe"}' \
                  '}]}'
    print(f'Original string: {simple_json}')
    escaped = simple_json.replace('"', '\\"')
    print(f'Escaped string: {escaped}')
    parsed_json = json.loads(simple_json)
    print(f'Parsed json: {parsed_json}')
