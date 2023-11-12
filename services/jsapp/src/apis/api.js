import axios from "axios";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { message } from "antd";

const instance = axios.create({
  baseURL: process.env.REACT_APP_API_ENDPOINT,
  timeout: 10000,
});

const STATUS_CODE = {
  UNAUTHORIZED: 401,
  BAD_REQUEST: 400,
  INTERNAL_SERVER_ERROR: 500,
};

const ERROR_MESSAGE = {
  LOGIN_EXPIRED: "Login Expired",
  NETWORK_ERROR: "Network Error",
};

const AxiosInterceptor = ({ children }) => {
  const navigate = useNavigate();
  const [isSet, setIsSet] = useState(false);
  const requestInterceptor = (config) => {
    const token = localStorage.getItem("token");
    if (
      typeof token !== "undefined" &&
      token !== null &&
      token !== "undefined"
    ) {
      config.headers["Authorization"] = `Bearer ` + token;
    } else {
      localStorage.clear();
      navigate("/login");
    }
    return config;
  };

  const requestInterceptorErrorHandler = (error) => Promise.reject(error);

  useEffect(() => {
    const resInterceptor = (response) => {
      if (response.data.code !== 200) {
        message.open({
          type: "error",
          content: response.data.message,
        });
      }
      return response;
    };

    const errInterceptor = (error) => {
      if (error.response) {
        switch (error.response.status) {
          case STATUS_CODE.UNAUTHORIZED:
            localStorage.clear();
            message.open({
              type: "error",
              content: ERROR_MESSAGE.LOGIN_EXPIRED,
            });
            navigate("/login");
            break;
          case STATUS_CODE.BAD_REQUEST:
            console.log("match 400");
            message.open({
              type: "error",
              content: error.response.data,
            });
            break;
          case STATUS_CODE.INTERNAL_SERVER_ERROR:
            message.open({
              type: "error",
              content: "Internal Error",
            });
            break;
          default:
            console.log("Unexpected status code", error.response.status);
            break;
        }
      }
      if (error.code === "ERR_NETWORK") {
        message.open({
          type: "error",
          content: ERROR_MESSAGE.NETWORK_ERROR,
        });
      }

      return new Promise(() => {});
    };

    const interceptor = instance.interceptors.response.use(
      resInterceptor,
      errInterceptor
    );

    instance.interceptors.request.use(
      requestInterceptor,
      requestInterceptorErrorHandler
    );
    setIsSet(true);

    return () => instance.interceptors.response.eject(interceptor);
  }, [navigate]);

  return isSet && children;
};

export default instance;
export { AxiosInterceptor };
