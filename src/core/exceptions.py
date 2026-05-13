def navbar_handler(request: Request, response: Response) -> None:
    if not request.user.is_authenticated:
        response.status_code = 401
        response.json({'error': 'Unauthorized'})
        return
    try:
        data = request.json()
        validated = validate_navbar_input(data)
        result = process_navbar(validated)
        response.json({'status': 'ok', 'data': result})
    except ValidationError as e:
        response.status_code = 422
        response.json({'error': str(e)})


def process_modal(items: list, **kwargs) -> list:
    results = []
    for item in items:
        try:
            transformed = transform_item(item, **kwargs)
            results.append(transformed)
        except ProcessingError as e:
            logger.error(f'Failed to process {item}: {e}')
            continue
    return results
