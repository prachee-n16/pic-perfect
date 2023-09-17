import { create } from "zustand";
import { useEffect, useState } from "react";
import type { RobotClient, StreamClient, BaseClient } from "@viamrobotics/sdk";
import {
    RobotCredentials,
    getRobotClient,
    getStreamClient,
    getBaseClient,
    getStream,
  } from "./client";

export type ClientStatus = "disconnected" | "loading" | "connected";

export interface Store {
    status: ClientStatus;
    client?: RobotClient;
    streamClient?: StreamClient;
    baseClient?: BaseClient;
    connectOrDisconnect: (credentials: RobotCredentials) => unknown;
  }
  
  export const useStore = create<Store>((set, get) => ({
    status: "disconnected",
    client: undefined,
    streamClient: undefined,
    baseClient: undefined,
    connectOrDisconnect: (credentials: RobotCredentials) => {
      const status = get().status;
      if (status === "disconnected") {
        console.log(`Currently disconnected, connecting...`);
        console.log("Setting state to 'loading'...");
        set({ status: "loading" });
  
        console.log(
          `Getting robot client for credentials ${JSON.stringify(
            credentials,
            null,
            2
          )}`
        );
        getRobotClient(credentials)
          .then((client) => {
            console.log(`Got client ${client}`);
            console.log(`Getting stream client`);
            const streamClient = getStreamClient(client);
            console.log(
              `Received stream client ${JSON.stringify(streamClient, null, 2)}`
            );
            console.log(`Getting base client`);
            const baseClient = getBaseClient(client);
            console.log(
              `Received base client ${JSON.stringify(baseClient, null, 2)}`
            );
            const stateUpdate = {
              status: "connected",
              client,
              baseClient,
              streamClient,
            };
            console.log(
              `Setting state to connected: ${JSON.stringify(
                stateUpdate,
                null,
                2
              )}`
            );
            //@ts-ignore
            set({ ...stateUpdate });
            console.log("Set state to connected");
          })
          .catch((error: unknown) => set({ status: "disconnected" }));
      } else if (status === "connected") {
        console.log(`Currently connected, disconnecting...`);
        set({ status: "loading" });
  
        get()
          ?.client?.disconnect()
          .then(() => set({ status: "disconnected" }))
          .catch((error: unknown) => set({ status: "disconnected" }));
      }
    },
  }));
  
  export const useStream = (
    streamClient: StreamClient | undefined,
    cameraName: string
  ): MediaStream | undefined => {
    const [streamLock, setStreamLock] = useState(false);
    const [stream, setStream] = useState<MediaStream | undefined>();
  
    useEffect(() => {
      if (streamClient && !streamLock) {
        console.log(
          `Fetching stream for camera "${cameraName}" because streamLock is ${streamLock} and streamClient is ${JSON.stringify(
            streamClient,
            null,
            2
          )}`
        );
  
        setStreamLock(true);
  
        getStream(streamClient, cameraName)
          .then((mediaStream) => setStream(mediaStream))
          .catch((error: unknown) => {
            console.warn(`Unable to connect to camera ${cameraName}`, error);
          });
  
        return () => {
          setStreamLock(false);
  
          streamClient.remove(cameraName).catch((error: unknown) => {
            console.warn(
              `Unable to disconnect to camera "${cameraName}". Caught the following error:`,
              error
            );
          });
        };
      }
  
      return undefined;
    }, [streamClient, cameraName]);
  
    return stream;
  };