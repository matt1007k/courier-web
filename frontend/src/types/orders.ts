export interface DetailState{
	id: number;
	tracking_code: string;
	contain: string;
	created_at_naturaltime: string;
	description: string;
	distance: string;
	get_tracking_code_text: string;
	image: string | null;
	price_rate: string;
	size: string;
	status: string;
	value: string;
	address_destiny: AddressState;
	address_origin: AddressState;
	order: OrderState;
}

export interface ClientState{
	cell_phone: string;
	driver_code: string;
	full_name: string;
	logo: string | null;
	slug: string;
	social_media: string | null;
	store_name: string | null;
	user: number;
}

export interface AddressState{
	id: number;
	address: string;
	address_city: string;
	address_complete: string;
	address_detail: string;
	address_gps: string | null;
	cell_phone: string;
	city: string;
	client: ClientState;
	default: boolean;
	district: string;
	email: string | null;
	full_name: string;
	reference: string | null;
}

export interface OrderState{
	id: number;
	igv: string | null;
	payed_image: string;
	promo_code: string | null;
	status: string;
	sub_total: string;
	total: string;
	type_ticket: string;
	client: ClientState;
}

export interface StatusState{
	label: string;
	status: string;
}