import styled from 'styled-components';

interface FilterContentProps{
	isShow: boolean;
}

export const FilterWrapper = styled.div`
	padding-bottom: 0.5rem;
`
export const FilterHeader = styled.div`
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 0.5rem 0;
`
export const FilterContent = styled.div<FilterContentProps>`
	display: ${props => props.isShow ? 'block' : 'none'};
	margin-top: 0.5rem;
	padding: 0.5rem;
`
export const FilterForm = styled.form`
	display: grid;
	grid-template-columns: 1fr;
	gap: 20px;
	margin-top: 0.5rem;

	@media (min-width: 768px) {
		grid-template-columns: repeat(4, 1fr);
	}
`