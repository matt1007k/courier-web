import React from 'react';
import { DetailState } from '../../types/orders';

import { DetailStatus } from './DetailStatus'
import Dropdown from "../Overlay/Dropdown";
import ModalBottom from "../Overlay/ModalBottom";

interface OrderItemProps{
	detail: DetailState;
}

const OrderItem: React.FC<OrderItemProps> = ({detail}) => (
	<div className="card card-normal order-list-row">
        <div className="order-list-col">
            <div className="icon icon-warning-default rounded rounded-md">
                <img src="/static/icon/order-icon.svg" />
            </div>
            <div className="content" style={{ alignItems: "flex-start" }}>
                <p className="text-small text-muted font-normal">{ detail.get_tracking_code_text }</p>
                <h6>{ detail.order.client.full_name }</h6>
                <div className="order-detail">
                    <p>{ detail.created_at_naturaltime }</p>
                </div>
            </div>
            <ModalBottom title="Acciones" target={
                <div className="cursor-pointer icon-view h6">
                    <i className='bx bx-dots-horizontal-rounded bx-sm'></i>
                </div>
            }>
                <div className="options">
                    <a href="#" className="option-item">
                        <span>Ver detalles</span>
                        <div className="icon ">
                            <i className='bx bx-show bx-sm'></i>
                        </div>
                    </a>
                </div>
            </ModalBottom>
        </div>
        <div className="order-list-col">
            <div className="text-small">{ detail.address_origin.address_complete }</div>
            <h6>{ detail.address_origin.full_name }</h6>
            <p className="flex items-center">
                <i className="bx bx-mobile-alt bx-xs" style={{ marginRight: "5px" }}></i>
                <span>{ detail.address_origin.cell_phone }</span>
            </p>
        </div>
        <div className="order-list-col">
            <div className="text-small">{ detail.address_destiny.address_complete }</div>
            <h6>{ detail.address_destiny.full_name }</h6>
            <p className="flex items-center">
                <i className="bx bx-mobile-alt bx-xs" style={{ marginRight: "5px" }}></i>
                <span>{ detail.address_destiny.cell_phone }</span>
            </p>
        </div>
        <div className="order-list-col">
            <DetailStatus status={detail.status} />
        </div>
        <div className="order-list-col" style={{ justifySelf: "end" }}>
            <Dropdown target={
                    <div className="cursor-pointer h6">
                        <i className='bx bx-dots-horizontal-rounded bx-sm'></i>
                    </div>
                }>
                <a href="#" className="dropdown-item-2">
                    <span>Seguimiento</span>
                    <i className='bx bx-list-check bx-sm'></i>
                </a>
            </Dropdown>
        </div>
    </div>	
);

export default React.memo(OrderItem);