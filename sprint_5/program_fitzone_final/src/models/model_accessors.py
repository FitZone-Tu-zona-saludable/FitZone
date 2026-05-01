"""Helpers para mantener entidades encapsuladas sin romper compatibilidad.

Las clases del proyecto ya eran usadas con atributos públicos por servicios,
controladores y pruebas. Este decorador conserva esa forma de uso mediante
properties, pero guarda los valores internamente en atributos protegidos.
También genera métodos get_<campo>() y set_<campo>(valor) para cada campo.
"""


def _build_property(field_name):
    private_name = f"_{field_name}"

    def getter(self):
        return getattr(self, private_name)

    def setter(self, value):
        setattr(self, private_name, value)

    return property(getter, setter)


def _build_getter(field_name):
    def getter(self):
        return getattr(self, field_name)

    return getter


def _build_setter(field_name):
    def setter(self, value):
        setattr(self, field_name, value)

    return setter


def encapsulated_model(cls):
    """Agrega properties y getters/setters a una entidad.

    Cada clase declara _fields. El decorador genera propiedades compatibles
    con los nombres públicos existentes y métodos get_/set_ consistentes.
    """
    for field_name in getattr(cls, "_fields", ()): 
        if not isinstance(getattr(cls, field_name, None), property):
            setattr(cls, field_name, _build_property(field_name))

        getter_name = f"get_{field_name}"
        if not hasattr(cls, getter_name):
            setattr(cls, getter_name, _build_getter(field_name))

        setter_name = f"set_{field_name}"
        if not hasattr(cls, setter_name):
            setattr(cls, setter_name, _build_setter(field_name))

    return cls
