import { createSlice } from "@reduxjs/toolkit";
import dominanceService from "../../services/dominanceService";

import { loadingStatus } from "../global/globalSlice";
import { toast } from "react-toastify";

export const checkUploadedFile = (param, status = true) => async (dispatch) => {
	dispatch(loadingStatus(true));
    return dominanceService
		.checkDominance(param)
		.then(async (res) => {
			if (res?.status === 200) {
				// if (status) {
				// 	dispatch(dominanceDetailSuccess(res?.data));				
				// }
				dispatch(dominanceDetailSuccess(res?.data));
			} else {
				if (status) {
					toast.error(res?.data?.message)
				}
			}
			return dispatch(loadingStatus(false));
		})
		.catch((error) => {
			dispatch(loadingStatus(false));
			return dispatch(dominanceDetailError(error));
		});
};

const initialState = {
	success: false,
	dominanceDetail: null
};

const checkDominance = createSlice({
	name: "dominance",
	initialState,
	reducers: {
		dominanceDetailSuccess: (state, action) => {
			state.success = true;
			state.dominanceDetail = action.payload;
		},
		dominanceDetailError: (state, action) => {
			state.success = false;
			state.dominanceDetail = null;
		},
	},
	extraReducers: {},
});

export const {
	dominanceDetailSuccess,
	dominanceDetailError
} = checkDominance.actions;

export default checkDominance.reducer;
