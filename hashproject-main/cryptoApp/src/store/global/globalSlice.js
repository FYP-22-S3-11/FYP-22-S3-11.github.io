import { createSlice } from '@reduxjs/toolkit';

const initialState = {
	loading: false,
};

const loadingSlice = createSlice({
	name: 'loading',
	initialState,
	reducers: {
		loadingStatus: (state, action) => {
			state.loading = action.payload
		},
	},
	extraReducers: {}
});

export const { loadingStatus } = loadingSlice.actions;

export default loadingSlice.reducer;
