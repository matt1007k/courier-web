import React, { createContext, useReducer } from 'react'
import { RoleState, PermissionState } from '../types/auth';

import AuthReducer, { ACTIONTYPES, AuthActions } from './AuthReducer'


export type initialAuthType = {
	permissions: PermissionState[];
	role: RoleState;
	isFetching: boolean;
	error: any;
}

export const initialRole: RoleState = {
	is_admin: false,
	is_driver: false,
	is_client: false,
};

export const initialAuthState = {
	permissions: [],
	role: initialRole,
	isFetching: false,
	error: false
}

export const AuthContext = createContext<{ state: initialAuthType; dispatch: React.Dispatch<AuthActions>}>({ state: initialAuthState, dispatch: () => null});

export const AuthContextProvider: React.FC = ({ children }) => {
	const [state, dispatch] = useReducer(AuthReducer, initialAuthState);

	return (
		<AuthContext.Provider value={{ state, dispatch }}>
			{children}
		</AuthContext.Provider>
	)
}