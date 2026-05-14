export function validateUtils(data: UtilsInput): ValidationResult {
    const errors: Record<string, string> = {};

    if (!data.email || !isValidEmail(data.email)) {
        errors.email = 'A valid email is required';
    }
    if (!data.password || data.password.length < 8) {
        errors.password = 'Password must be at least 8 characters';
    }

    return {
        valid: Object.keys(errors).length === 0,
        errors,
    };
}
