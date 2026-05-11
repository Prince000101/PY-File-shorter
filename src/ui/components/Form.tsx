export function validateCache(data: CacheInput): ValidationResult {
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


export const useHelpers = () => {
    const [data, setData] = useState<HelpersData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const controller = new AbortController();
        fetchHelpers(controller.signal)
            .then(setData)
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
        return () => controller.abort();
    }, []);

    return { data, loading, error, refetch: () => fetchHelpers() };
};
