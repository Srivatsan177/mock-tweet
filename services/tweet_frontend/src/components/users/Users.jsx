import { Box, TextField, FormControl, Button } from "@mui/material";
import { useEffect, useState } from "react"
import UserProfile from "./UserProfile";
import { usersGet } from "../../utils/api";
import { SearchOutlined } from "@mui/icons-material";

function Users() {
    const [usersProfile, setUsersProfile] = useState([]);
    const [searchUsername, setSearchUsername] = useState("");

    const handleSubmit = (e) => {
        console.log(searchUsername);
        e.preventDefault();
        usersGet({ username: searchUsername }).then(response => {
            setUsersProfile(response.data)
            console.log(response.data)
        }
        ).catch((err) => console.log(err));
    }

    return (
        <Box sx={{ margin: "2% 15%" }}>
            <FormControl sx={{ width: "100%" }}>
                <TextField
                    id="outlined-basic"
                    label="Username"
                    value={searchUsername}
                    onChange={(e) => setSearchUsername(e.target.value)}
                    variant="outlined"
                />
                <Button onClick={handleSubmit}><SearchOutlined /></Button>
            </FormControl>
            {usersProfile.length ? usersProfile.map((user, idx) => <UserProfile key={idx} userProfile={user} />) : "No result found"}
        </Box>
    )
}

export default Users