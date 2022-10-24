import { createSlice } from "@reduxjs/toolkit";
import cryptoService from "../../services/cryptoService";
import { loadingStatus } from "../global/globalSlice";
import { toast } from "react-toastify";

export const getCryptoDetail = (param, status = true) => async (dispatch) => {
	dispatch(loadingStatus(true));
	return cryptoService
		.getCoinDetail(param)
		.then(async (res) => {
			if (res?.data?.code === 200) {
				if (status) {
					toast.success("Add successfully")
				}
				dispatch(cryptoDetailSuccess(res?.data));
			} else {
				if (status) {
					toast.error(res?.data?.message)
				}
			}

			return dispatch(loadingStatus(false));
		})
		.catch((error) => {
			dispatch(loadingStatus(false));
			return dispatch(cryptoDetailError(error));
		});
};

const initialState = {
	success: false,
	cryptoDetail: null
};

const cryptoSlice = createSlice({
	name: "crypto",
	initialState,
	reducers: {
		cryptoDetailSuccess: (state, action) => {
			state.success = true;
			state.cryptoDetail = action.payload;
		},
		cryptoDetailError: (state, action) => {
			state.success = false;
			state.cryptoDetailList = null;
		},
	},
	extraReducers: {},
});

export const {
	cryptoDetailSuccess,
	cryptoDetailError
} = cryptoSlice.actions;

export default cryptoSlice.reducer;
