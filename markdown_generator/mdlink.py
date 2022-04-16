def link(url, text=None):
    if url:
        return f'[{text}]({url})' if text else url
    return ''
