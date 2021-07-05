import React, { FormEvent, useEffect, useState, useContext } from 'react'
import { FilterWrapper, FilterHeader, FilterContent, FilterForm } from './styles';

import { AuthContext } from '../../../context/AuthContext';
import { getPermissions } from '../../../api/authApi'

export interface FilterFormState{
	q: string;
	origin: string;
	destiny: string;
	date_from: string;
	date_to: string;
	type_ticket: string;
}

interface FilterAdvancedProps {
	onSubmitForm: (form: FilterFormState) => void;
	status: string;
}

const FilterAdvanced: React.FC<FilterAdvancedProps> = ({ onSubmitForm, status }) => {
	const [show, setShow] = useState<boolean>(false);

	const [q, setQ] = useState<string>('');
	const [origin, setOrigin] = useState<string>('');
	const [destiny, setDestiny] = useState<string>('');
	const [date_from, setDateFrom] = useState<string>('');
	const [date_to, setDateTo] = useState<string>('');
	const [type_ticket, setTypeTicket] = useState<string>('');
    const { state, dispatch } = useContext(AuthContext);

    useEffect(() => {
        getPermissions(dispatch);
    }, [])

	const onSubmit = (event: FormEvent<HTMLFormElement>) => {
		event.preventDefault();
		onSubmitForm({q, origin, destiny, date_from, date_to, type_ticket});
	};

	const setClean = () => {
		setQ('');
		setOrigin('');
		setDestiny('');
		setDateFrom('');
		setDateTo('');
		setTypeTicket('');
		onSubmitForm({q: '', origin: '', destiny: '', date_from: '', date_to: '', type_ticket: ''});
	}

	const getParamsFilter = () => {
		return '?' + (new URLSearchParams({
			status,
			q,
			origin,
			destiny,
			date_from,
			date_to,
			type_ticket
		})).toString();
	}
	
	const exportPDF = () => {
		window.location.href = '/orders/exportPDF/' + getParamsFilter();
	}

	const exportExcel = () => {
		window.location.href = '/orders/exportExcel/' + getParamsFilter();
	}

	return (
		<FilterWrapper>
			<FilterHeader>
				<button className="btn btn-default btn-small" onClick={() => setShow(!show)}>
					<i className='bx bx-sm bx-slider-alt'></i>
					<span>Filtrar</span>
				</button>
				<div style={{marginLeft: '20px', display: 'flex', overflowX: 'auto'}}>
					{ state.role.is_admin && <>
						<button 
							style={{ marginRight: '4px', padding: '8px', background: '#f40f02'}}
							className="btn btn-danger btn-small" 
							onClick={() => exportPDF()}
							>
							<i className='bx bxs-file-pdf bx-sm'></i>
							<span>PDF</span>
						</button>
						<button 
							style={{ padding: '8px', background: '#1d6f42', color: 'white'}}
							className="btn btn-success btn-small" 
							onClick={() => exportExcel()}
							>
							<i className='bx bxs-file bx-sm'></i>
							<span>Excel</span>
						</button>
					</>}
				</div>
			</FilterHeader>
			<FilterContent isShow={show}>
				<h6>Búsqueda avanzada</h6>
				<FilterForm onSubmit={onSubmit}>
					<div className="form-group">
						<label htmlFor="search"># tracking o cliente</label>
						<input
							type='search'
							name='q'
							id='search'
							placeholder="Buscar por # seguimiento o datos del cliente"
							className="input"
							style={{ padding: '14px' }} 
							onChange={(e) => setQ(e.target.value)} 
							value={q} />
					</div>
					<div className="form-group">
						<label htmlFor="origin">Dirección recojo</label>
						<input 
							type='search' 
							name='origin' 
							id='origin' 
							placeholder="Buscar por distrito, datos de la persona"
							className="input" 
							style={{ padding: '14px' }} 
							onChange={(e) => setOrigin(e.target.value)} 
							value={origin} />
					</div>
					<div className="form-group">
						<label htmlFor="destiny">Dirección envío</label>
						<input 
							type='search' 
							name='destiny' 
							id='destiny' 
							placeholder="Buscar por distrito, datos de la persona"
							className="input" 
							style={{ padding: '14px' }} 
							onChange={(e) => setDestiny(e.target.value)} 
							value={destiny} />
					</div>
					<div className="form-group">
						<label htmlFor="type_ticket">Comprobante electrónico</label>
						<select 
							name='type_ticket' 
							id='type_ticket' 
							className="input" 
							style={{ padding: '14px' }} 
							onChange={(e) => setTypeTicket(e.target.value)} 
							value={type_ticket}>
								<option value="">--- Seleccionar ---</option>
								<option value="BOLETA">BOLETA</option>
								<option value="FACTURA">FACTURA</option>
						</select>
					</div>
					<div className="form-group">
						<label htmlFor="date_from">Fecha de</label>
						<input 
							type="date" 
							className="input" 
							name="date_from" 
							id="date_from" 
							style={{ padding: '11px' }} 
							onChange={(e) => setDateFrom(e.target.value)} 
							value={date_from} />
					</div>
					<div className="form-group">
						<label htmlFor="date_to">Fecha hasta</label>
						<input 
							type="date" 
							className="input" 
							name="date_to" 
							id="date_to" 
							style={{ padding: '11px' }} 
							onChange={(e) => setDateTo(e.target.value)} 
							value={date_to} />
					</div>
					<div style={{ alignSelf: 'center'}}>
						<button className="btn btn-primary btn-small btn-full" type="submit">Buscar</button>
					</div>
					<div style={{ alignSelf: 'center'}}>
						<button className="btn btn-default btn-small btn-full" type="button" onClick={setClean}>Limpiar campos</button>
					</div>
				</FilterForm>
			</FilterContent>
		</FilterWrapper>
	);

};

export default FilterAdvanced;