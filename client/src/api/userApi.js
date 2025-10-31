import axiosClient from "./axiosClient";

export const getUsers = async () => {
  const res = await axiosClient.get("/users_list");
  return res.data;
};

export const getMyAttendance = async () => {
  const res = await axiosClient.get("/attendance/me");
  return res.data;
};
