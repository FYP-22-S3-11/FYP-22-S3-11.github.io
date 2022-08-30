import React, { useEffect, useState, useCallback } from "react";
import { useDispatch } from "react-redux";
import { toast } from "react-toastify";
import { ReactSearchAutocomplete } from 'react-search-autocomplete'
import Table from 'react-bootstrap/Table';
// import { getCryptoList, } from "../store/crypto/cryptoSlice";
import { loadingStatus } from "../store/global/globalSlice";
import cryptoService from "../services/cryptoService";

/**
 * @returns html
 */
const Home = () => {
    const dispatch = useDispatch();

    const [cryptoList, setCryptoList] = useState([])
    const [list, selectedList] = useState([])
    const [searchText, setSearchText] = useState('')
    const [searchIteam, setSearchIteam] = useState(null)

    const getDetailApiCall = useCallback((id, status = false) => {
        cryptoService.getCoinDetail(id).then((i) => {
            selectedList([...list, i?.data?.data])
            if (status) {
                toast.success("Add successfully")
                setSearchText('')
                setSearchIteam(null)
            }
            dispatch(loadingStatus(false));

        }).catch(() => {
            if (status) {
                toast.error("Internal Server Error");
            }
            dispatch(loadingStatus(false));
        })
    }, [dispatch, list])

    useEffect(() => {
        dispatch(loadingStatus(true));
        if (list?.findIndex(i => i?.name.trim() === "Bitcoin") === -1) {
            getDetailApiCall({ name: 'Bitcoin', type: 'coin' })
        }
        cryptoService.getAlgoList().then((i) => {
            setCryptoList(i?.data?.data)
            dispatch(loadingStatus(false));

        }).catch(() => {
            // toast.error("Internal Server Error");
            dispatch(loadingStatus(false));
        })

    }, [dispatch, getDetailApiCall, list]);


    const addCrypto = (id) => {

        dispatch(loadingStatus(true));
        if (list?.findIndex(i => i?.name.trim() === id.name) === -1) {
            getDetailApiCall(id, true)
        } else {
            toast.error("Already Added");
            dispatch(loadingStatus(false));

        }


    }

    const handleOnSearch = (string, results) => {
        setSearchText(string)
    }

    const handleOnSelect = (item) => {

        setSearchIteam(item?.data)
    }

    const addCryptoToList = () => {
        if (searchIteam) {
            addCrypto(searchIteam)
        }
    }

    return (
        <div className="">

            <div className="comparsion-tbl-wrap">

                <div className="searchbar-wrapper">
                    <h2 className="text-light">Comparsion Table</h2>

                    <div className="search-box" >

                        <ReactSearchAutocomplete
                            items={cryptoList?.map((i, index) => ({ id: index, data: i, name: i.name }))}
                            inputSearchString={searchText}
                            onSearch={handleOnSearch}
                            onSelect={handleOnSelect}
                            autoFocus
                            style={{
                                border: '1px solid #D1D1D1',
                                borderRadius: ' 15px',
                            }}
                        />


                    </div>
                    <div className="search-action">
                        <button type="button" onClick={() => addCryptoToList()} className="btn btn-primary ">Compare Now</button>
                    </div>
                </div>
                <Table className="comparsion-table  text-light">
                    <tbody>
                        {list?.map((i, index) => (
                            <tr key={index}>
                                <td>{index + 1} <img width={20} src={i?.img} alt={i?.name} /> <span className="result">{i?.name}</span></td>
                                <td>
                                    <div className="value-label">Price (USD)</div>
                                    <span className="text-light">  {i?.symbol} <span className="result">{i?.price}</span></span>
                                    <span className={`markit-stat ${i?.percent.includes('-') ? 'negative' : ''}`}>{i?.percent}</span>
                                </td>
                                <td>
                                    <div className="value-pairs">
                                        <div className="value-label">Hash</div>
                                        <span className="result">{i?.algo}</span>
                                    </div>
                                </td>
                                <td>
                                    <div className="value-pairs">
                                        <div className="value-label">Market Cap (24h)</div>
                                        <span className="result">{i?.marketcap}</span>
                                    </div>
                                </td>
                                <td>
                                    <div className="value-pairs">
                                        <div className="value-label">Features</div>
                                        <ul className="feature-list">
                                            <li>Volume - {i?.volume}</li>
                                        </ul>
                                    </div>
                                </td>
                            </tr>

                        ))}

                    </tbody>
                </Table>
            </div>
        </div>
    )
}

export default Home