import { get } from './../utils/request';
import { PermissionState } from '../types/auth';
import { useEffect, useState } from 'react'


export const useCanPermission = () => {
	const [permissions, setPermissions] = useState<PermissionState[]>([]);

	const loadPermissions = () => {
		get('/auth/api/permissions-auth/', )
			.then((data) => {
				setPermissions(data);
				console.log(data);
			});
	}
	
	const can = (codename: string) => {
		loadPermissions();
				console.log(permissions);
		return permissions.some(permission => permission.codename === codename); 
	}
	
	return [
		permissions,
		can
	];
};