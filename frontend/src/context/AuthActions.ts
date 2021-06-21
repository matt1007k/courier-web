import { AuthState } from '../types/auth'

export const FetchStart = () => ({
	type: 'fetch_start',
});

export const FetchSuccess = (data: AuthState) => ({
	type: 'fetch_success',
	payload: data,
});

export const FetchError = (error: any) => ({
	type: 'fetch_error',
	payload: error
});