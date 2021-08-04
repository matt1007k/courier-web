export interface UserState {
  full_name?: string;
  email: string;
  username: string;
  avatar: string;
}

export interface PermissionState {
  name?: string;
  codename: string;
}

export interface RoleState {
  is_admin: boolean;
  is_driver: boolean;
  is_client: boolean;
}

export interface AuthState {
  user: UserState;
  permissions: PermissionState[];
  role: RoleState;
}
