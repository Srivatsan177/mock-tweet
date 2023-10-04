import { Box, FormControl, TextField, Typography, Button } from "@mui/material";
import { useEffect, useState } from "react";
import { signin } from "../../utils/api";
import { useNavigate } from "react-router";
import Cookies from "js-cookie"

export default function SignIn() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate()
  useEffect(() => { Cookies.remove("jwt") }, []);
  async function handleSubmit() {
    if (await signin(username, password)) {
      navigate("/")
    }
  }
  return (
    <Box
      sx={{
        "& .MuiTextField-root": { marginBottom: "1em" },
        textAlign: "center",
        margin: "1em",
      }}
    >
      <Typography variant="h6">SignIn</Typography>
      <FormControl sx={{
        backgroundColor: "#fff",
        padding: "1em",
        margin: "1em",
      }}
      >
        <TextField label="Username" variant="outlined" value={username} onChange={(val) => setUsername(val.target.value)} />
        <TextField label="Password" variant="outlined" type="password" value={password} onChange={(val) => setPassword(val.target.value)} />
        <Button color="success" onClick={handleSubmit} variant="outlined">Login</Button>
      </FormControl>
    </Box>
  )
}
