import { createSlice } from "@reduxjs/toolkit";
import hashService from "../../services/hashService";
import { loadingStatus } from "../global/globalSlice";


export const getHashList = () => async (dispatch) => {
	dispatch(loadingStatus(true));
	return hashService.getList()
		.then(async (res) => {
			dispatch(cryptoSuccess(res?.data));
			return dispatch(loadingStatus(false));
		})
		.catch((error) => {
			dispatch(loadingStatus(false));
			return dispatch(cryptoError(error));
		});
};

const initialState = {
	success: false,
	hash: null,
};

const hashSlice = createSlice({
	name: "hash",
	initialState,
	reducers: {
		hashSuccess: (state, action) => {
			state.success = true;
			state.hashList = action.payload;
		},

		hashDetailSuccess: (state, action) => {
			state.success = true;
			state.hashDetail = action.payload;
		},

		hashError: (state, action) => {
			state.success = false;
			state.hashList = null;
		},
		hashDetailError: (state, action) => {
			state.success = false;
			state.hashDetailList = null;
		},
	},
	extraReducers: {},
});

export const {
	cryptoSuccess,
	cryptoError,
	cryptoDetailSuccess,
	cryptoDetailError

} = hashSlice.actions;

export default hashSlice.reducer;
