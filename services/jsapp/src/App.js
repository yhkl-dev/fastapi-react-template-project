import "./App.css";
import React, { useEffect } from "react";
import SericeAccounts from "./components/sericeAccounts";
import { Routes, Route } from "react-router-dom";
import Login from "./login";
import DefaultLayout from "./layout";
import { AxiosInterceptor } from "./apis/api";
import { useDispatch } from "react-redux";
import { setResponse } from "./components/responseSlice.js";

function App() {
  const dispatch = useDispatch();
  const authenticate = () => {
    const baseURL = process.env.REACT_APP_API_ENDPOINT;
    const params = new URLSearchParams(window.location.search);
    const authToken = params.get("authToken");
    window.history.pushState("object", document.title, "/");

    if (authToken) {
      localStorage.setItem("token", authToken);
      sendRequest(baseURL + "login", "Bearer " + authToken);
    } else {
      sendRequest(baseURL + "user-session-status/");
    }
  };

  const sendRequest = (url, authToken = "") => {
    const request = {
      method: "GET",
      headers: authToken ? { Authorization: authToken } : {},
      credentials: "include",
    };

    fetch(url, request)
      .then((response) => response.json())
      .then((data) => {
        dispatch(setResponse(data));
      })
      .catch((err) => {
        console.error("Request failed", err);
      });
  };

  useEffect(() => {
    authenticate();
  });

  return (
    <AxiosInterceptor>
      <Routes>
        <Route path="/" element={<DefaultLayout />}>
          <Route index element={<SericeAccounts />}></Route>
        </Route>
        <Route path="/login" element={<Login />}></Route>
      </Routes>
    </AxiosInterceptor>
  );
}

export default App;
