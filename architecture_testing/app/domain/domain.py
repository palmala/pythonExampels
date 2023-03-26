from ..data import datasource


class Domain:

    @classmethod
    def get_transformed_data(cls):
        result = datasource.Datasource.get_data()
        if result['status'] == 'successful':
            return result['message'].upper()
