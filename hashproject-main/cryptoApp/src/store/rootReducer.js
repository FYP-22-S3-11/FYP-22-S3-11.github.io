import { combineReducers } from '@reduxjs/toolkit';
import global from './global/globalSlice';
import crypto from './crypto/cryptoSlice';
import hash from './hash/hashSlice'
import dominance from './dominance/checkDominance'

/**
 * Define Root reducer
 * @param {*} asyncReducers 
 * @returns reducer
 */
const createReducer = asyncReducers => (state, action) => {
	const combinedReducer = combineReducers({
		global,
		crypto,
		hash,
		dominance,
	});


	return combinedReducer(state, action);
};


export default createReducer;
