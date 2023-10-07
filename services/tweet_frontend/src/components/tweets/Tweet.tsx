import {
  Box,
  CardContent,
  Typography,
  Card,
  CardActions,
  Button,
  ButtonBase,
  CardMedia,
} from "@mui/material";
import {
  AccountCircleOutlined,
  FavoriteBorderOutlined,
  Favorite,
  Share,
  ChatBubbleOutlineOutlined,
} from "@mui/icons-material";
import { useNavigate } from "react-router";
import TweetAction from "./TweetAction";
import { imagesGet, post } from "../../utils/api";
import { useEffect, useState } from "react";
export default function Tweet({
  id,
  username,
  tweet,
  like,
  liked_by_user,
  image_name,
  mutate,
}: {
  id: string;
  username: string;
  tweet: string;
  like: Number;
  liked_by_user: Boolean;
}) {
    const handleLike = async (id: string) => {
        await post(`/like-tweet/${id}`)
        mutate()
    }
  const navigate = useNavigate();
  const [imageUrl, setImageURL] = useState(null);
  useEffect(() => {
    // @ts-ignore
    const fn =async () => {
      if (image_name){
        const s3_url = await imagesGet(`/get-s3-url/${id}`, { image_name: image_name });
        setImageURL(s3_url)
      }
    }
    fn()
  }, [])
  return (
    <Box
      sx={{
        display: "block",
        marginBottom: "1em",
        marginTop: "1em",
        padding: "0.1em",
        backgroundColor: "#abc",
        borderRadius: "1em",
      }}
    >
      <Card
        variant="outlined"
        sx={{
          backgroundColor: "#fff",
          borderRadius: "1em",
        }}
      >
        <CardContent
          sx={{ cursor: "pointer" }}
        >
          <Typography variant="h5" onClick={() => navigate("/user", {state: {username}})}>
            <AccountCircleOutlined />
            {username}
          </Typography>
          <hr />
          {imageUrl && <CardMedia component="img" sx={{ width: "25%", height:"auto" }} image={imageUrl} />}
          <Typography onClick={() => navigate(`/tweet/${id}`)} component="pre" variant="h6">
            {tweet}
          </Typography>
        </CardContent>
        <CardActions>
          <TweetAction
            handleClick={() => handleLike(id)}
            icon={
              liked_by_user ? (
                <Favorite color="error" />
              ) : (
                <FavoriteBorderOutlined color="error" />
              )
            }
            count={like}
          />
          <Button color="success">
            <Share />
          </Button>
          <Button color="inherit" onClick={() => navigate(`/tweet/${id}`, { state: { autofocus: true } })}>
            <ChatBubbleOutlineOutlined />
          </Button>
        </CardActions>
      </Card>
    </Box>
  );
}
