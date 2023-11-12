import { createSlice } from "@reduxjs/toolkit";

const responseSlice = createSlice({
  name: "response",
  initialState: null,
  reducers: {
    setResponse: (state, action) => action.payload,
  },
});

export const { setResponse } = responseSlice.actions;

export default responseSlice.reducer;
