import { useEffect, useState } from "react"
import { userGet } from "../../utils/api";
import { Button, Card, CardActions, CardContent, Typography } from "@mui/material";
import { useLocation } from "react-router";

function UserProfile({ userProfile=null }) {
    const [user, setUser] = useState(userProfile ? { ...userProfile } : {});
    const { state } = useLocation();
    useEffect(() => {
        if (!user) {
            userGet({ username: state?.username }).then((response) => {
                setUser(response.data);
            }
            ).catch(error => console.log(error));
        }
    }, [])

    return (
        <Card sx={{ margin: "2% 15%" }}>
            <CardContent>
                <Typography variant="h5">
                    Username: {user?.username}
                </Typography>
                <hr />
                <Typography variant="body2">
                    Name: {user?.name}
                </Typography>
                <Typography variant="body2">
                    email: {user?.email}
                </Typography>
            </CardContent>
            <CardActions>
                <Button sx={{ paddingBottom: 0 }}>Followers</Button> {user?.followers?.length}
                <Button sx={{ paddingBottom: 0 }}>Following</Button> {user?.followers?.length}
            </CardActions>
        </Card>
    )
}

export default UserProfile