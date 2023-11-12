import instance from "./api";

export const getServiceAccount = (params) => {
  return instance({
    url: "api/accounts",
    method: "get",
    params,
  });
};

export const createServiceAccount = (params) => {
  return instance({
    url: "api/accounts",
    method: "post",
    data: params,
  });
};

export const updateServiceAccount = (id, params) => {
  return instance({
    url: "api/accounts/" + id,
    method: "put",
    data: params,
  });
};

export const deleteServiceAccount = (id) => {
  return instance({
    url: "api/accounts/" + id,
    method: "delete",
  });
};
