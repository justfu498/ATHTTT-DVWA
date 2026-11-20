def output_encode(value):
    if value is None:
        return ''

    table = {
        '&': '&amp;',
        '<': '&lt',
        '>': '&gt',
        '"': '&quot;',
        "'": '&#x27;'
    }
    return ''.join([table.get(ch, ch) for ch in str(value)])