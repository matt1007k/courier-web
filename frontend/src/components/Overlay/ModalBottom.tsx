import React, { useState } from 'react'

interface ModalBottomProps {
	title: string;	
	target: React.ReactNode;
}

const ModalBottom:React.FC<ModalBottomProps> = ({ title, target, children }) => {  
	const [open, setOpen] = useState<boolean>(false);

	return (
		<>
			<div onClick={() => setOpen(true)} className="cursor-pointer">
				{target}
			</div>
			{ open && 
			<div className="modal modal-sheet">
				<div className="modal-content card" style={{ width: "100%" }}>
					<div className="head">
						<h6>{ title }</h6>
						<div className="close">
							<button onClick={() => setOpen(false)} className="btn btn-default btn-circle btn-small">
								<i className='bx bx-x bx-sm'></i>
							</button>
						</div>
					</div>
					<div className="form-modal">
						{ children }
					</div>
				</div>
			</div>
			}
		</>
	);

};

export default ModalBottom;