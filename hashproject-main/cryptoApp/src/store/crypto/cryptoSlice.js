import { createSlice } from "@reduxjs/toolkit";
import cryptoService from "../../services/cryptoService";
import { loadingStatus } from "../global/globalSlice";


export const getCryptoList = () => async (dispatch) => {
	dispatch(loadingStatus(true));
	return cryptoService
		.getCryptoList()
		.then(async (res) => {
			dispatch(cryptoSuccess(res?.data));
			return dispatch(loadingStatus(false));
		})
		.catch((error) => {
			dispatch(loadingStatus(false));
			return dispatch(cryptoError(error));
		});
};

export const getCryptoDetail = (param) => async (dispatch) => {
	dispatch(loadingStatus(true));
	return cryptoService
		.getCryptoDetail(param)
		.then(async (res) => {
			dispatch(cryptoDetailSuccess(res?.data));
			return dispatch(loadingStatus(false));
		})
		.catch((error) => {
			dispatch(loadingStatus(false));
			return dispatch(cryptoDetailError(error));
		});
};



const initialState = {
	success: false,
	cryptoList: null,
	cryptoDetail: null
};

const cryptoSlice = createSlice({
	name: "crypto",
	initialState,
	reducers: {
		cryptoSuccess: (state, action) => {
			state.success = true;
			state.cryptoList = action.payload;
		},

		cryptoDetailSuccess: (state, action) => {
			state.success = true;
			state.cryptoDetail = action.payload;
		},

		cryptoError: (state, action) => {
			state.success = false;
			state.cryptoList = null;
		},
		cryptoDetailError: (state, action) => {
			state.success = false;
			state.cryptoDetailList = null;
		},
	},
	extraReducers: {},
});

export const {
	cryptoSuccess,
	cryptoError,
	cryptoDetailSuccess,
	cryptoDetailError

} = cryptoSlice.actions;

export default cryptoSlice.reducer;
