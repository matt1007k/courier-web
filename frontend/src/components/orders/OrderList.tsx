import React, { useState, useEffect } from "react";
import { render } from "react-dom";
import { get } from "../../utils/request";

import { DetailState } from "../../types/orders";
import { PaginationState } from "../../types/pagination";

import OrderItem from "./OrderItem";
import { FilterStatus } from "./FilterStatus";
import FilterAdvanced, { FilterFormState } from "./FilterAdvanced";
import Pagination from '../Navigation/Pagination';

import { AuthContextProvider } from '../../context/AuthContext';

const OrderList: React.FC = () => {
  const [orders, setOrders] = useState<DetailState[]>([]);
  const [isFetching, setFetching] = useState<boolean>(false);
  const [status, setStatus] = useState<string>('');
  const [link, setLink] = useState<PaginationState>({page: 1, total: 0, lastPage: 0, perPage: 10, start: 0, end:10});


  const loadData = (page: number = 1, status: string = '', form: FilterFormState = { 
    q: '',
    origin: '',
    destiny: '',
    date_from: '', 
    date_to: '',
    type_ticket: '',
  }) => {
    setFetching(true);
     get('/details/api/', { page, status, ...form })
      .then(data => {
        setFetching(false);
        setOrders(data.data);
        setLink({...data.links});
      });
  }

  const changePage = (currentPage: number) => {
    loadData(currentPage, status);
  };

  const filterByStatus = (type: string) => {
    setStatus(type);
    loadData(1, type);
  }

  useEffect(loadData, [])

  const onSubmit = (form: FilterFormState) => {
    loadData(1, status, form);
  }

  return (
    <>
      <FilterStatus status={status} onStatus={filterByStatus} />
      <FilterAdvanced onSubmitForm={onSubmit} status={status} />
      { isFetching 
        ?  <div>Cargando...</div>
        : (<div className="mb-10 order-list-grid">
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
            {link.total > 0 
              && <>
              { orders.map((detail, index) => (
                  <OrderItem key={index} detail={detail} />
                ))}
                {link.lastPage > 1 && <Pagination link={link} onPageChange={changePage} />}
               </>}
              {link.total == 0 && <div className="card text-muted">Sin pedidos registados</div>}
          </div>)
      }
    </>
  );
}

export default React.memo(OrderList);

const container = document.getElementById("orders");
render(
  <AuthContextProvider>
    <OrderList />
  </AuthContextProvider>
, container);
