import {
    BrowserRouter as Router,
    useRoutes,
} from 'react-router-dom';

import React from "react";
import { useSelector } from "react-redux";
import Spinner from 'react-bootstrap/Spinner';
import Header from "../component/header"
import Home from "../page/home";


/**
 * Define the rounting
 * @returns Route
 */

function AppRoutes() {
    const routes = useRoutes(
        [
            { path: '/', element: <Home /> },
        ]
    )
    return routes;
}

const IndexRoute = () => {
    const loading = useSelector(({ global }) => global.loading);
    return (
        <>
            {loading && <div className="loader">
                <Spinner animation="border" variant="primary" />
            </div>
            }
            <Header />
            <div className='container-fluid'>
                <Router basename='/crytopcompare/'>
                    <AppRoutes />

                </Router>
            </div>
        </>
    );
};
export default IndexRoute;
