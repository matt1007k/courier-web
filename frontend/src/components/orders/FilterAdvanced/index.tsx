import React, { FormEvent, useEffect, useState, useContext } from 'react'
import { FilterWrapper, FilterHeader, FilterContent, FilterForm } from './styles';

import { AuthContext } from '../../../context/AuthContext';
import { getPermissions } from '../../../api/authApi'
import { can } from '../../../utils/authorization';

export interface FilterFormState{
	q: string;
	origin: string;
	destiny: string;
	date: string;
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
	const [date, setDate] = useState<string>('');
    const { state, dispatch } = useContext(AuthContext);

    useEffect(() => {
        getPermissions(dispatch);
    }, [])

	const onSubmit = (event: FormEvent<HTMLFormElement>) => {
		event.preventDefault();
		onSubmitForm({q, origin, destiny, date});
	};

	const setClean = () => {
		setQ('');
		setOrigin('');
		setDestiny('');
		setDate('');
		onSubmitForm({q: '', origin: '', destiny: '', date: ''});
	}

	const getParamsFilter = () => {
		return '?' + (new URLSearchParams({
			status,
			q,
			origin,
			destiny,
			date,
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
							placeholder="Buscar por distrito, datos de la persona"
							className="input" 
							style={{ padding: '14px' }} 
							onChange={(e) => setDestiny(e.target.value)} 
							value={destiny} />
					</div>
					<div className="form-group">
						<label htmlFor="date">Fecha de registro</label>
						<input 
							type="date" 
							className="input" 
							name="date" 
							id="date" 
							style={{ padding: '11px' }} 
							onChange={(e) => setDate(e.target.value)} 
							value={date} />
					</div>
					<button className="btn btn-primary btn-small" type="submit">Buscar</button>
					<button className="btn btn-default btn-small" type="button" onClick={setClean}>Limpiar campos</button>
				</FilterForm>
			</FilterContent>
		</FilterWrapper>
	);

};

export default FilterAdvanced;