def get_class(dottedname):
    parts = dottedname.split('.')

    module_name = '.'.join(parts[0:-1])
    class_name = parts[-1]

    module = import_module(module_name)
    return getattr(module, class_name)


def import_module(name):
    module = __import__(name)
    components = name.split('.')
    for components in components[1:]:
        module = getattr(module, components)
    return module
