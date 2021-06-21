export interface PermissionState{
	name?: string;
	codename: string;
}

export interface RoleState{
	is_admin: boolean;
	is_driver: boolean;     
	is_client: boolean;     
}

export interface AuthState{
	permissions: PermissionState[];
	role: RoleState;
}