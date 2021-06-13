import React from 'react'

interface DetailStatusProps {
	status: string;
}
interface badgeTypeState{
	[index: string]: {
		type: string;
		label: string;
	}; 
}

export const DetailStatus:React.FC<DetailStatusProps> = ({status}) => {
	const badgeType: badgeTypeState = {
		'PE': {  type: 'warning', label: 'Pendiente'},
		'RE': { type: 'success', label: 'Recepcionado'},
		'AL': { type: 'primary', label: 'Almacén'},
		'ER': { type: 'secondary', label: 'En ruta'},
		'EN': { type: 'success', label: 'Entregado'},
		'NEN': { type: 'warning', label: 'No entregado'},
		'REPR': { type: 'success', label: 'Reprogramado'},
	};	
	const type = badgeType[status].type;
	const label = badgeType[status].label;
	
	return (
	<>
		<span className={`badge badge-${type}`}>{label}</span>
	</>
	);
};