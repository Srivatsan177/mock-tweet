import axios from "axios";
import Cookies from "js-cookie"

const axiosInstance = axios.create({
    baseURL: "http://localhost:8080",
    timeout: 10000,
});

const axiosImageInstance = axios.create({
    baseURL: "http://localhost:8081/images",
    timeout: 10000,
});

axiosInstance.interceptors.request.use((config) => {
    config["headers"] = {...config["headers"], "Authorization": Cookies.get("jwt")}
    return config
});

axiosImageInstance.interceptors.request.use((config) => {
    config["headers"] = {...config["headers"], "Authorization": Cookies.get("jwt")}
    return config
});


const axiosUserInstance = axios.create(
    {
        baseURL: `${import.meta.env.VITE_USER_HOST}/user`,
        timeout: 10000,
    }
);

axiosUserInstance.interceptors.request.use((config) => {
    config["headers"] = {...config["headers"], "Authorization": Cookies.get("jwt")}
    return config
});

export async function get(path: string) {
    const response = await axiosInstance.get(path)
    return response.data;
}

export async function post(path: string, data: any = {}) {
    const response = await axiosInstance.post(path, data)
    return response.data
}

export async function signin(username: string, password: string) {
    try{
        const response = await axiosInstance.post("/users/signin", {username, password})
        Cookies.set("jwt", response.data.jwt)
        return true     
    } catch (error) {
        console.log(error)
        return false
    }
}

export async function imagesGet(path: string, data: any) {
    const response = await axiosImageInstance.get(path, { params: data })
    return response.data
}

export async function imagesPost(url: string, data: any = {}) {
    await axios.put(url, data)
}

export async function userGet(data: any) {
    return await axiosUserInstance.get("", {params: {search_username: data.username}});
}

export async function usersGet(data: any) {
    return await axiosUserInstance.get("/list", {params: {search_username: data.username}});
}