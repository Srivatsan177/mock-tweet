import React from "react";
import { Box, Button } from "@mui/material";

export default function TweetAction({
  icon,
  count,
  handleClick,
}: {
  icon: React.ReactElement;
  count: Number;
  handleClick: Function;
}) {
  return (
    <Box
      sx={{
        "& .MuiBox-root": { display: "inline", margin: "0", padding: "0" },
        margin: "0",
        padding: "0",
      }}
    >
      <Box>
        <Button onClick={handleClick}>{icon}</Button>
      </Box>
      <Box>
        <Button disabled sx={{ fontSize: "1.5em" }}>
          {String(count)}
        </Button>
      </Box>
    </Box>
  );
}
