import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';

import "./style/App.css";
import IndexRoute from "./router/route";
import { Provider } from "react-redux";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { PersistGate } from "redux-persist/integration/react";

import { store, persistor } from "./store";
// import Interceptor from "./utils/interceptors";
// Interceptor(store);

const App = () => {
  return (
    <div className="main-contain">
      <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}>
          <IndexRoute />
          <ToastContainer />
        </PersistGate>
      </Provider>
    </div>
  );
};

export default App;
