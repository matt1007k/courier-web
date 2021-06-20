import { initialAuthState } from "./AuthContext";

export type ACTIONTYPES = 
	| { type: 'fetch_start', payload: any }
	| { type: 'fetch_success', payload: any }
	| { type: 'fetch_error', payload: any }

const AuthReducer = (state: typeof initialAuthState, action: ACTIONTYPES) => {
	switch(action.type){
		case 'fetch_start':
			return { 
				permissions: [],
				isFetching: true,
				error: false
			}
		case 'fetch_success':
			return { 
				permissions: action.payload,
				isFetching: false,
				error: false
			}
		case 'fetch_error':
			return { 
				permissions: [],
				isFetching: false,
				error: action.payload
			}
		default:
			return state;
	}
};

export default AuthReducer;