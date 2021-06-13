import React, { useEffect, useState } from 'react'
import { StatusState } from '../../types/orders';

interface FilterStatusProps {
	status: string;
	onStatus: (type: string) => void;
}

export const FilterStatus:React.FC<FilterStatusProps> = ({status, onStatus}) => {
	const [statuses, setStatuses] = useState<StatusState[]>([]);
	
	useEffect(() => {
		fetch('/details/api/statuses/')
			.then(res => res.json())
			.then(data => setStatuses(data));
	}, [])

	return (
	<div className="filter-list">
		<button onClick={() => onStatus('')} className={`btn btn-${status == '' ? 'primary' : 'link' } btn-rounded btn-small`}>Todos</button>
		{statuses.map((dbstatus, index) => (
			<a key={index} onClick={() => onStatus(dbstatus.status)}  className={`btn btn-${status == dbstatus.status ? 'primary' : 'link'} btn-rounded btn-small`}>{ dbstatus.label }</a>
		))}
	</div>
	);
};