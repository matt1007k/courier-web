import React, { FormEvent, useState } from 'react'
import { FilterWrapper, FilterHeader, FilterContent, FilterForm } from './styles';

export interface FilterFormState{
	q: string;
	origin: string;
	destiny: string;
	date: string;
}

interface FilterAdvancedProps {
	onSubmitForm: (form: FilterFormState) => void;
}

const FilterAdvanced: React.FC<FilterAdvancedProps> = ({ onSubmitForm }) => {
	const [show, setShow] = useState<boolean>(false);

	const [q, setQ] = useState<string>('');
	const [origin, setOrigin] = useState<string>('');
	const [destiny, setDestiny] = useState<string>('');
	const [date, setDate] = useState<string>('');

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

	return (
		<FilterWrapper>
			<FilterHeader>
				<button className="btn btn-default btn-small" onClick={() => setShow(!show)}>
					<i className='bx bx-sm bx-slider-alt'></i>
					<span>Filtrar</span>
				</button>
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