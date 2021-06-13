import React from 'react'
import { PaginationState } from '../../types/pagination';

interface PaginationProps {
	link: PaginationState;
	onPageChange: (currentPage: number) => void;
}

const Pagination:React.FC<PaginationProps> = ({link, onPageChange}) => (
    <div className="mb-10 table-list-bottom">
         <div className="table-list-details">
             <p>
                 Viendo del
                 <span className="font-medium"> { link.start } </span>
                 al
                 <span className="font-medium"> { link.end } </span>
                 de
                 <span className="font-semibold"> { link.total } </span>
                 resultados
             </p>
         </div>
         <div className="pagination space-x">
			{ link.page > 1 
			? <button onClick={() => onPageChange(link.page - 1)} className="cursor-pointer pagination-item">Anterior</button>
			: <button className="pagination-item disable">Anterior</button> }
			{Array.from(Array(link.lastPage), (e, i) => {
			if (link.page == (i + 1)){
				return <button key={i} className="pagination-item page-number active">{ i + 1 }</button>
			}else{
				return <button key={i} onClick={() => onPageChange(i + 1)} className="cursor-pointer pagination-item page-number">{ i + 1 }</button>
			}
			})}

			{ link.page < link.lastPage 
			? <button onClick={() => onPageChange(link.page + 1)} className="cursor-pointer pagination-item">Siguiente</button>
			: <button className="pagination-item disable">Siguiente</button> }

         </div>
    </div>
);

export default React.memo(Pagination);