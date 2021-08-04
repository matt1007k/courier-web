import React, { createContext, useReducer } from "react";
import { RoleState, PermissionState, UserState } from "../types/auth";

import AuthReducer, { ACTIONTYPES, AuthActions } from "./AuthReducer";

export type initialAuthType = {
  user: UserState;
  permissions: PermissionState[];
  role: RoleState;
  isFetching: boolean;
  error: any;
};

export const initialUser: UserState = {
  full_name: "",
  email: "",
  username: "",
  avatar: "/static/img/avatar.png",
};

export const initialRole: RoleState = {
  is_admin: false,
  is_driver: false,
  is_client: false,
};

export const initialAuthState = {
  user: initialUser,
  permissions: [],
  role: initialRole,
  isFetching: false,
  error: false,
};

export const AuthContext = createContext<{
  state: initialAuthType;
  dispatch: React.Dispatch<AuthActions>;
}>({ state: initialAuthState, dispatch: () => null });

export const AuthContextProvider: React.FC = ({ children }) => {
  const [state, dispatch] = useReducer(AuthReducer, initialAuthState);

  return (
    <AuthContext.Provider value={{ state, dispatch }}>
      {children}
    </AuthContext.Provider>
  );
};
