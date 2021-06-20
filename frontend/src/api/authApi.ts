import { get } from './../utils/request';

export const getPermissions = async (dispatch: any) => {
	dispatch({ type: 'fetch_start' });
	try {
		const data = await get('/auth/api/permissions-auth/')
		dispatch({ type: 'fetch_success', payload: data });
	} catch (error) {
		dispatch({ type: 'fetch_error', payload: error });
	}
}