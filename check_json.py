from register import Registry

register_check = Registry('check')


@register_check.register()
def check_imageData(json_file):
    imageData = json_file['imageData']
    assert imageData is None
    return True
