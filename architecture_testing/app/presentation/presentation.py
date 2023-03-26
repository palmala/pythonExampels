from ..domain import domain


class Presentation:

    @classmethod
    def get_json(cls):
        return {'result': domain.Domain.get_transformed_data()}
