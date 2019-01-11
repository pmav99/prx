from cleo import Command as BaseCommand
import munch
import schema


class Command(BaseCommand):

    schema = None

    def get_parameters(self):
        """ Return command parameters """
        params = {
            **{key: self.option(key) for key in self._config.options},
            **{key: self.argument(key) for key in self._config.arguments},
        }
        return params

    def parse_parameters(self, validate=True):
        params = self.get_parameters()
        if isinstance(self.schema, schema.Schema) and validate:
            try:
                params = self.schema.validate(params)
            except schema.SchemaError:
                # TODO hide SchemaErrors from the end user.
                # we need to raise an issue, in a way that cleo will understand it.
                raise
        return munch.munchify(params)

    def __init__(self):
        super().__init__()
