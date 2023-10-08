import { Modal, Box, Typography, FormControl, TextField, Button, Input } from "@mui/material";
import { CloudUpload } from "@mui/icons-material";
import { useState } from "react";
import { post, imagesGet, imagesPost } from "../../utils/api";
import { styled } from '@mui/material/styles';
import axios from "axios";

const style = {
    position: "absolute",
    textAlign: "center",
    left: "40%",
    width: "20%",
    top: "40%",
    padding: "1em",
    backgroundColor: "#fff",
}
const VisuallyHiddenInput = styled('input')({
    clip: 'rect(0 0 0 0)',
    clipPath: 'inset(50%)',
    height: 1,
    overflow: 'hidden',
    position: 'absolute',
    bottom: 0,
    left: 0,
    whiteSpace: 'nowrap',
    width: 1,
  });

export default function AddTweet({ open, handleClose }) {
    const [tweet, setTweet] = useState("");
    const [imageFile, setImageFile] = useState();
    async function handleSubmit(e) {
        e.preventDefault()
        console.log(e)
        const tempTweet = await post("/tweet", { tweet })
        if (imageFile){
            const formData = new FormData()
            const s3_url = await imagesGet(`/get-s3-url/${tempTweet.id}`, { image_name: imageFile.name })
            formData.append(imageFile.name, imageFile)
            await await fetch(s3_url, {
                method: "PUT",
                body: imageFile,
                headers: {
                    "Content-Type": imageFile.type,
                }
            })
            setImageFile(undefined)
        }
        setTweet("")
        handleClose(false)
    }
    return (
        <Modal
            open={open}
            onClose={handleClose}
        >
            <Box
                sx={style}
            >
                <Typography variant="h6">Post a Tweet</Typography>
                <form onSubmit={handleSubmit}>
                    <FormControl>
                        <TextField multiline required sx={{ marginBottom: "1em" }} value={tweet} rows="4" onChange={(e) => setTweet(e.target.value)} label="Tweet"></TextField>
                        <Button sx={{ marginBottom: "1em" }} component="label" variant="contained" startIcon={<CloudUpload />}>
                            Upload Image
                            <VisuallyHiddenInput onChange={(e) => setImageFile(e.target.files[0])} type="file" />
                        </Button>
                        <Button color="primary" type="submit" variant="outlined">Tweet</Button>
                    </FormControl>
                </form>
            </Box>
        </Modal>
    )
}
