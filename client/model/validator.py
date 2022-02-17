"""the file will contains the payload validator for the apis."""

from client.exceptions import PayloadTypeError


def array_of_string_vali(field_name: str, field_value: list) -> None:
    """the function will validate the input <field_value> is a list of string can be extend as a class."""

    if type(field_value) != list:
        raise PayloadTypeError('payload `%s` should be <list> but recieved %s' % (field_name, type(field_value)))
    for v in field_value:
        if type(v) != str:
            raise PayloadTypeError('payload `%s` should be <string list>' % (field_name))

    return
