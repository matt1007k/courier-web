import { ActionMap } from "../types/reducer";
import { initialAuthType, initialUser } from "./AuthContext";
import { initialRole } from "./AuthContext";

export enum Types {
  start = "fetch_start",
  success = "fetch_success",
  error = "fetch_error",
}

type AuthPayload = {
  [Types.start]: initialAuthType;
  [Types.success]: initialAuthType;
  [Types.error]: initialAuthType;
};

export type ACTIONTYPES =
  | { type: "fetch_start"; payload: any }
  | { type: "fetch_success"; payload: any }
  | { type: "fetch_error"; payload: any };

// const AuthReducer = (state: typeof initialAuthState, action: ACTIONTYPES) => {
export type AuthActions = ActionMap<AuthPayload>[keyof ActionMap<AuthPayload>];

const AuthReducer = (state: initialAuthType, action: AuthActions) => {
  switch (action.type) {
    case "fetch_start":
      return {
        user: initialUser,
        permissions: [],
        role: initialRole,
        isFetching: true,
        error: false,
      };
    case "fetch_success":
      return {
        user: action.payload.user,
        permissions: action.payload.permissions,
        role: action.payload.role,
        isFetching: false,
        error: false,
      };
    case "fetch_error":
      return {
        user: initialUser,
        permissions: [],
        role: initialRole,
        isFetching: false,
        error: action.payload,
      };
    default:
      return state;
  }
};

export default AuthReducer;
