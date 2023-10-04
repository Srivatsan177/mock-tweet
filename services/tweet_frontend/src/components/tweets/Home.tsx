import { get } from "../../utils/api"
import { useNavigate } from "react-router";
import Tweet from "./Tweet";
import { Box, Fab, Grid } from "@mui/material";
import { Add } from "@mui/icons-material";
import AddTweet from "./AddTweet";
import { useEffect, useState } from "react";
import useSWR from "swr";

export default function Home() {
    const [open, setOpen] = useState(false);
    // const [rows, setRows] = useState([]);
    const navigate = useNavigate()
    // useEffect(() => {
    //     async function fetchData() {
    //         try{
    //             const data = await get("/");
    //             setRows(data);
    //         } catch(error){
    //             navigate("/login")
    //         }
    //     }
    //     fetchData()
    // }, [open])
    const {data: rows, isLoading, error, mutate: mutateTweet} = useSWR("/", get)
    if (isLoading) return <>Loading...</>
    else if (error) navigate("/login")

    return (
        <> 
            {rows.map(row => <Tweet key={row.id} {...row} mutate={mutateTweet} />)}
            <Fab
                sx={{
                    position: "fixed",
                    bottom: 0,
                    right: 0,
                    margin: "1em",
                    padding: "1em",
                }}
                onClick={() => setOpen(true)}
                color="primary"
            >
                <Add />
            </Fab>
            <AddTweet handleClose={() => {
                setOpen(false)
            }} open={open} />
        </>
    )
}
