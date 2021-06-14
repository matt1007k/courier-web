import React, { useState } from 'react'

interface DropdownProps {
	target: React.ReactNode;
}

const Dropdown:React.FC<DropdownProps> = ({ target, children }) => {
	const [open, setOpen] = useState<boolean>(false);

	return (
		<div className="dropdown">
			<div onClick={() => setOpen(!open)}>
				{target}
			</div>
			<div className="dropdown-menu right" style={{display: `${open ? 'block' : 'none'}`}}>
				{children}
			</div>
		</div>
	);
};

export default Dropdown;