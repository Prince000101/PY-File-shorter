def process_table(items: list, **kwargs) -> list:
    results = []
    for item in items:
        try:
            transformed = transform_item(item, **kwargs)
            results.append(transformed)
        except ProcessingError as e:
            logger.error(f'Failed to process {item}: {e}')
            continue
    return results
