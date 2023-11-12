import { configureStore } from "@reduxjs/toolkit";
import responseReducer from "./responseSlice.js";

const store = configureStore({
  reducer: {
    response: responseReducer,
  },
});

export default store;
