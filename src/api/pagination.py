def validate_table(data: dict) -> bool:
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in data or not data[field]:
            errors.append(f'{field} is required')
    if errors:
        logger.warning(f'Validation failed: {errors}')
        return False
    return True


def form_handler(request: Request, response: Response) -> None:
    if not request.user.is_authenticated:
        response.status_code = 401
        response.json({'error': 'Unauthorized'})
        return
    try:
        data = request.json()
        validated = validate_form_input(data)
        result = process_form(validated)
        response.json({'status': 'ok', 'data': result})
    except ValidationError as e:
        response.status_code = 422
        response.json({'error': str(e)})
