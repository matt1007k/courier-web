import React, { useState, useEffect, useContext } from "react";
import { render } from "react-dom";
import { get } from "../../utils/request";

import { DetailState } from "../../types/orders";
import { PaginationState } from "../../types/pagination";

import OrderItem from "./OrderItem";
import { FilterStatus } from "./FilterStatus";
import Pagination from '../Navigation/Pagination';

import { AuthContext, AuthContextProvider } from '../../context/AuthContext';
import { getPermissions } from '../../api/authApi'

const OrderList: React.FC = () => {
  const [orders, setOrders] = useState<DetailState[]>([])
  const [status, setStatus] = useState<string>('');
  const [link, setLink] = useState<PaginationState>({page: 1, total: 0, lastPage: 0, perPage: 10, start: 0, end:10});
  const { state, dispatch } = useContext(AuthContext);


  const loadData = (page: number = 1, status: string = '') => {
     get('/details/api/', { page, status })
      .then(data => {
        setOrders(data.data);
        setLink({
          page: data.page, 
          perPage: data.per_page, 
          total: data.total, 
          lastPage: data.last_page, 
          start: data.start, 
          end: data.end
        });
      });
    getPermissions(dispatch);
  }

  const changePage = (currentPage: number) => {
    loadData(currentPage, status);
  };

  const filterByStatus = (type: string) => {
    setStatus(type);
    loadData(1, type);
  }

  useEffect(loadData, [])

  return (
    <>
    {JSON.stringify(state.permissions)}
      <FilterStatus status={status} onStatus={filterByStatus} />
      <div className="mb-10 order-list-grid">
        <div className="order-list-head">
            <div className="order-list-head-item">
                Detalles del pedido
            </div>
            <div className="order-list-head-item">
                Dirección de recojo
            </div>
            <div className="order-list-head-item">
                Dirección de envío
            </div>
            <div className="order-list-head-item">
                Estado
            </div>
            <div className="order-list-head-item" style={{ justifySelf: 'end'}}>
                Acciones
            </div>
        </div>
        {orders.map((detail, index) => (
          <OrderItem key={index} detail={detail} />
        ))}
        <Pagination link={link} onPageChange={changePage} />
      </div>
    </>
  );
}

export default OrderList;

const container = document.getElementById("orders");
render(
  <AuthContextProvider>
    <OrderList />
  </AuthContextProvider>
, container);
