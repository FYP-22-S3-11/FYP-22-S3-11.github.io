import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { checkUploadedFile } from "../../store/dominance/checkDominance";
import { dominanceDetailSuccess  } from "../../store/dominance/checkDominance";
import Table from 'react-bootstrap/Table';
import BarChart from 'react-bar-chart';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUpload, faTv, faShield, faFile, faPercent } from '@fortawesome/free-solid-svg-icons'

/**
 * @returns html
 */
const CheckDominance = () => {
    const dispatch = useDispatch();
    const [fileItem, setFileItem] = useState([]) 
    const dominanceDetail = useSelector(({ dominance }) => dominance?.dominanceDetail)

    useEffect(() => {
        dispatch(dominanceDetailSuccess(null))
    }, [dispatch])

    const handleFileUpload = (string, results) => {
        const files = string?.target?.files;
        var all_files =[]
        for (let i =0 ;i<files.length;i++) {
            all_files.push(files[i])
        }
        setFileItem(all_files)
    }

    const checkNow = () => {
        if(fileItem) {
            dispatch(checkUploadedFile(fileItem))
        }
    }
    const margin = {top: 50, right: 20, bottom: 50, left: 40};


    function Visualization(data) {   
        return( 
            <BarChart ylabel='Time(0-1s)'
                    width={300                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      }
                    height={500}
                    margin={margin}
                    data={data?.data}
                    />
       )
    }
    

    return (
        <div className="">
            <div className="comparsion-tbl-wrap">
                <div className="searchbar-wrapper">
                    <div className="search-box">
                    <FontAwesomeIcon icon={faUpload} />   
                    <input
                        type="file"
                       className="upload-input"
                        multiple="multiple"
                        onChange={handleFileUpload}
                    />
                     <span>Choose a file...</span>                  
                    </div>
                    <div className="search-action">
                        <button type="button" onClick={() => checkNow()} className="btn btn-primary ">Check Now</button>
                    </div>                      
                </div>

                {/* Tab section starts */}
                {dominanceDetail && dominanceDetail?.result ?
                    <ul class="nav nav-pills nav-fill my-4" id="pills-tab" role="tablist">
                        <li class="nav-item tab-btn" role="presentation">
                            <button class="nav-link" id="pills-viz-tab" data-bs-toggle="pill" 
                            data-bs-target="#pills-viz" type="button" role="tab" aria-controls="pills-viz" 
                            aria-selected="true">
                            <div className="my-2"> 
                                <FontAwesomeIcon icon={faTv} />
                                </div>
                                Visualization
                            </button>
                        </li>
                        <li class="nav-item tab-btn" role="presentation">
                            <button class="nav-link" id="pills-security-tab" data-bs-toggle="pill" data-bs-target="#pills-security" type="button" role="tab" aria-controls="pills-security" aria-selected="false">
                                        <div className="my-2"> 
                                        <FontAwesomeIcon icon={faShield} />
                                        </div>
                                Security Leak
                                </button>
                        </li>
                        <li class="nav-item tab-btn" role="presentation">
                            <button class="nav-link" id="pills-dominant-tab" data-bs-toggle="pill" data-bs-target="#pills-dominant" type="button" role="tab" aria-controls="pills-dominant" aria-selected="false">
                                        <div className="my-2"> 
                                        <FontAwesomeIcon icon={faFile} />
                                        </div>
                                Dominant Fn
                                </button>
                        </li>
                        <li class="nav-item tab-btn" role="presentation">
                            <button class="nav-link" id="pills-info-tab" data-bs-toggle="pill" data-bs-target="#pills-info" type="button" role="tab" aria-controls="pills-info" aria-selected="false">
                                        <div className="my-2"> 
                                        <FontAwesomeIcon icon={faPercent} /> 
                                        </div>
                                More Info
                                </button>
                        </li>
                    </ul>
                :
                    ''
                }
                <div class="tab-content" id="pills-tabContent">
                    <div class="tab-pane fade show active" id="pills-viz" role="tabpanel" aria-labelledby="pills-viz-tab">
                    {/* Visulization tab starts */}
                    <div className="container">
                            <div className="row  justify-content-center align-items-center">
                                <div className="col-12 col-lg-10">
                                    { dominanceDetail?.result?.visualization_data?.length > 0 ?
                                        <Visualization data ={dominanceDetail?.result?.visualization_data} />
                                    :

                                    <h1 className="text-white text-center">Please upload js file, zip file</h1>
                                    }
                                    </div>
                            </div>
                        </div>
                        {/* Visualization tab ends */}
                    </div>

                    <div class="tab-pane fade" id="pills-security" role="tabpanel" aria-labelledby="pills-security-tab">
                        {/* Security leak tab starts */}
                            
                        <div className="table-responsive">
                        <table class="table table-dark table-striped table-bordered">
                            <thead>
                                {/* Security Leaks Details */}
                            </thead>
                            {dominanceDetail?.result ?
                            // ?.optimization?.length !== 0 ?
                                <tbody>
                                    <tr>
                                    <th scope="row">File name</th>
                                    <th scope="row">Line no.</th>
                                    <th scope="row">Security Leak</th>
                                    </tr>

                                    {dominanceDetail?.result?.secret_data?.length !== 0  ?
                                        <tr>
                                        <td class="table-active">{dominanceDetail?.result?.fileName}</td>
                                        <td>{dominanceDetail?.result?.secret_data?.lineNo}</td>
                                        </tr>
                                    :  
                                        // console.log("-------------else") 
                                    
                                        Object.entries(dominanceDetail?.result?.optimization)?.map(([k,v],index) => (
                                            <tr key={index}>
                                                <td class="table-active">{k}</td>
                                                {v?.secret_data ?
                                                <>
                                                <td>{v?.secret_data?.lineNo}</td>
                                                <td>YES</td>
                                                </>
                                                :
                                                <>
                                                <td>--</td>
                                                <td>NO</td>
                                                </>
                                                }
                                                
                                            </tr>
                                        )
                                        
                                        )
                                    }
                                </tbody>
                            :
                                ''
                            }
                        </table>
                        </div>
                    {/* security leak tab ends here */}
                    </div>

                    <div class="tab-pane fade" id="pills-dominant" role="tabpanel" aria-labelledby="pills-dominant-tab">
                        {/* ... */}
                        {console.log("------------")}
                        <table class="table table-dark table-striped table-bordered">
                        <thead>
                            {/* Details */}
                        </thead>
                        <tbody>
                            <tr>
                            <th scope="row">Method/Function</th>
                            <th scope="row">Time consumed</th>
                            <th scope="row">Dominant</th>
                            </tr>
                            { dominanceDetail?.result?.methods.length > 0 ?
                                dominanceDetail?.result?.methods?.map((data,index) => ( 
                                <tr key={index}>
                                    {console.log("---------datya", data)}
                                    <td class="table-active">{data?.method}</td>
                                    <td>{data?.time}</td>
                                    <td>
                                    {dominanceDetail?.result?.max['time'] === data['time'] ?
                                    'YES'
                                    :
                                    'No'
                                    }
                                    </td>
                                </tr>
                                ))
                                :
                                <tr>
                                    <td class="table-active" colSpan={3}>No data found</td>
                                </tr>
                            }
                        </tbody>
                        </table>
                        {/*  */}
                    </div>

                    <div class="tab-pane fade" id="pills-info" role="tabpanel" aria-labelledby="pills-info-tab">
                        <div className="table-responsive">
                        {dominanceDetail?.result?.fileType === 'js' ?
                            <table class="table table-dark table-striped table-bordered">
                                <thead>
                                    Details
                                </thead>
                                <tbody>
                                    <tr>
                                    <th scope="row">File Name</th>
                                    <th scope="row">Optimization</th>
                                    <th scope="row">Time</th>
                                    <th scope="row">Rating</th>
                                    </tr>
                                    <tr>                                      
                                    <td class="table-active">{dominanceDetail?.result?.fileName}</td>
                                    <td>
                                        <ul className="feature-list" style={{'color': '#9f9090'}}>
                                            {Object.entries(dominanceDetail?.result?.optimization)?.map(([k,v], index) => (
                                                <li key={index}>{v}</li>
                                            ))}                                        
                                        </ul>
                                    </td>
                                    <td>{dominanceDetail?.result?.time ? `${dominanceDetail?.result?.time}` : '-'} </td>
                                    <td>{dominanceDetail?.result?.rate ? `${dominanceDetail?.result?.rate}` : '-'} </td>
                                </tr>
                                </tbody>
                            </table>
                        :
                            ''
                        }
                        {dominanceDetail?.result?.fileType === 'zip' ?
                            <table class="table table-dark table-striped table-bordered">
                                <thead>
                                    {/* Details */}
                                </thead>
                                <tbody>
                                    <tr>
                                    <th scope="row">File Name</th>
                                    <th scope="row">Optimization</th>
                                    <th scope="row">Time</th>
                                    <th scope="row">Rating</th>
                                    </tr>
                                    {Object.entries(dominanceDetail?.result?.optimization)?.map(([k,v], index) => (
                                        <tr>
                                            {console.log("--------------vvvvv",v)}
                                            <td class="table-active">{v?.fileName}</td>
                                            <td>
                                                <ul className="feature-list" style={{'color': '#9f9090'}}>
                                                    {Object.entries(v?.optimization)?.map(([k1,v1], index) => (
                                                        <li key={index}>{v1}</li>
                                                    ))}                                        
                                                </ul>
                                            </td>
                                            <td>{v?.time ? `${v?.time}` : '-'} </td>
                                            <td>{v?.rate ? `${v?.rated}` : '-'} </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        :
                            ''
                        }
                        </div> 
                    </div>
                </div>                                    
            </div>
          
        </div>
    )
}

export default CheckDominance