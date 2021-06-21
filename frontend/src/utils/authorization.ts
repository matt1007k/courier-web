import { PermissionState } from '../types/auth';

export const can = (permissions: PermissionState[], codename: string) => {
	return permissions.some(permission => permission.codename === codename);
}