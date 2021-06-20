import { PermissionState } from '../types/auth'

export const FetchStart = () => ({
	type: 'fetch_start',
});

export const FetchSuccess = (permissions: PermissionState) => ({
	type: 'fetch_success',
	payload: permissions,
});

export const FetchError = (error: any) => ({
	type: 'fetch_error',
	payload: error
});