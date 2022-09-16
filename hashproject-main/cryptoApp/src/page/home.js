import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { toast } from "react-toastify";
import { ReactSearchAutocomplete } from 'react-search-autocomplete'
import Table from 'react-bootstrap/Table';
import { getHashList, } from "../store/hash/hashSlice";
import { loadingStatus } from "../store/global/globalSlice";
import { getCryptoDetail, cryptoDetailSuccess } from "../store/crypto/cryptoSlice"

/**
 * @returns html
 */
const Home = () => {
    const dispatch = useDispatch();
    const hashlist = useSelector(({ hash }) => hash?.hashList);
    const cryptoDetail = useSelector(({ crypto }) => crypto?.cryptoDetail)
    const [list, selectedList] = useState([])
    const [searchText, setSearchText] = useState('')
    const [searchIteam, setSearchIteam] = useState(null)
    const [status, setStatus] = useState(true)

    useEffect(() => {
        dispatch(cryptoDetailSuccess(null))
        selectedList([])
    }, [dispatch])

    useEffect(() => {
        if (cryptoDetail) {
            selectedList([...list, {
                name: cryptoDetail?.data?.name,
                percent: cryptoDetail?.data?.percent,
                symbol: cryptoDetail?.data?.symbol,
                marketcap: cryptoDetail?.data?.marketcap,
                hash: cryptoDetail?.data?.hash,
                img: cryptoDetail?.data?.img,
                volume: cryptoDetail?.data?.volume
            }])

            setSearchText('')
            setSearchIteam(null)
            dispatch(cryptoDetailSuccess(null))
        }
    }, [dispatch, cryptoDetail, list])

    useEffect(() => {
        dispatch(getHashList())
    }, [dispatch])

    useEffect(() => {
        dispatch(getCryptoDetail({ name: 'Bitcoin', type: 'coin' }, false))
        setStatus(false)
    }, [dispatch, status]);


    const addCrypto = (id) => {
        dispatch(loadingStatus(true));
        if (list?.findIndex(i => (i?.name?.trim().toLowerCase() === id.name.toLowerCase() || i?.hash?.trim().toLowerCase() === id.name.toLowerCase())) === -1) {
            dispatch(getCryptoDetail(id))
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
                            items={hashlist?.data?.map((i, index) => ({ id: index, data: i, name: i?.name?.toLowerCase() }))}
                            inputSearchString={searchText}
                            onSearch={handleOnSearch}
                            onSelect={handleOnSelect}
                            autoFocus
                            style={{
                                border: '1px solid #D1D1D1',
                                borderRadius: '15px',
                            }}
                        />
                    </div>
                    <div className="search-action">
                        <button type="button" onClick={() => addCryptoToList()} className="btn btn-primary ">Compare Now</button>
                    </div>
                </div>
                <Table className="comparsion-table text-light">
                    <tbody>

                        {/* obj.arr.filter((value, index, self) =>
  index === self.findIndex((t) => (
    t.place === value.place && t.name === value.name
  ))
) */}

                        {list?.filter((value, index, self) =>
                            index === self.findIndex((t) => (
                                t.name === value.name
                            ))
                        )?.map((i, index) => (
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
                                        <span className="result">{i?.hash}</span>
                                    </div>
                                </td>
                                <td>
                                    <div className="value-pairs">
                                        <div className="value-label">Market Cap</div>
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