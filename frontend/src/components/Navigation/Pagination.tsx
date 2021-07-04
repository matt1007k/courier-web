import React from 'react'
import { PaginationState } from '../../types/pagination';

interface PaginationProps {
	link: PaginationState;
	onPageChange: (currentPage: number) => void;
}

const Pagination:React.FC<PaginationProps> = ({link, onPageChange}) => {
	const getPages = () => {
		const thisPage = link.page || 1;
		const pagesToShow = 6;
		const pages: number[] = [];

		pages.push(thisPage);

		for (let i = 0; i < pagesToShow - 1; i++) {
			if (pages.length < pagesToShow){
				if (Math.min.apply(null, pages) > 1){
					pages.push(Math.min.apply(null, pages) - 1);
				}
			}
			if (pages.length < pagesToShow){
				if (Math.max.apply(null, pages) < link.lastPage){
					pages.push(Math.max.apply(null, pages) + 1);
				}
			}

		}
		pages.sort((a, b) => a - b);

		return pages;
	}
	
	return (
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
				{ getPages().map((pageNum, i) => {
					if (link.page == pageNum){
						return <button key={i} className="pagination-item page-number active">{ pageNum }</button>
					}else{
						return <button key={i} onClick={() => onPageChange(pageNum)} className="cursor-pointer pagination-item page-number">{ pageNum }</button>
					}
				})}

				{ link.page < link.lastPage 
				? <button onClick={() => onPageChange(link.page + 1)} className="cursor-pointer pagination-item">Siguiente</button>
				: <button className="pagination-item disable">Siguiente</button> }

			</div>
		</div>
	);
}

export default React.memo(Pagination);