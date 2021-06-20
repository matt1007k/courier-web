import React, { createContext, useReducer } from 'react'

import AuthReducer, { ACTIONTYPES } from './AuthReducer'

export const initialAuthState = {
	permissions: [],
	isFetching: false,
	error: false
}

export const AuthContext = createContext<{ state: typeof initialAuthState; dispatch: React.Dispatch<ACTIONTYPES>}>({ state: initialAuthState, dispatch: () => null});

export const AuthContextProvider: React.FC = ({ children }) => {
	const [state, dispatch] = useReducer(AuthReducer, initialAuthState);

	return (
		<AuthContext.Provider value={{ state, dispatch }}>
			{children}
		</AuthContext.Provider>
	)
}