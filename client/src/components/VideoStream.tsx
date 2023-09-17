import { useStream } from "../state";
import { StreamClient } from "@viamrobotics/sdk";
import { useRef, useEffect, type ReactNode, FC, useState } from "react";

export interface VideoStreamProps {
    streamClient: StreamClient;
  }

  
const VideoStream: FC<VideoStreamProps> = ({ streamClient }): JSX.Element => {
    const stream = useStream(streamClient, "cam");
    const videoRef = useRef<HTMLVideoElement>(null);
    const [count, setCount] = useState(0);
  
    useEffect(() => {
      console.log("stream", stream);
      if (videoRef.current && stream) {
        console.log("We have a stream");
        videoRef.current.srcObject = stream;
        setCount(count + 1); // hack to force a re-render when we have a video stream so the video element will show up
      } else {
        console.log("We don't have a stream");
      }
    }, [stream]);
  
    return (
      <div className="flex flex-col space-y-2 p-4">
        <label>Camera Feed</label>
        <video
          className="border-2 border-gray-500"
          ref={videoRef}
          autoPlay
          muted
        />
      </div>
    );
  };
  export default VideoStream;