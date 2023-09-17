import { RobotCredentials } from "../client";
import { useStore } from "../state";
import React, { FC, useEffect, useState } from "react";
import VideoStream from "./VideoStream";

const demo_robot = {
    name: "Demo Rover",
    hostname: "dashboard-rover-main.nw1175dvmu.viam.cloud",
    secret: "j0eu0txhqx9csvgy05a49pn082etgb7qshw40w2lgpgttvbo",
  };

  interface DemoPageProps {
    // Define props and propTypes here
  }
  
  const DemoPage: FC<DemoPageProps> = (props) => {
    console.log(window);
    const { status, connectOrDisconnect, streamClient } = useStore();
  
    const handleConnectButton = () => {
      const demoRobotCredentials = {
        hostname: "dashboard-rover-main.nw1175dvmu.viam.cloud",
        secret: "j0eu0txhqx9csvgy05a49pn082etgb7qshw40w2lgpgttvbo",
      };
      connectOrDisconnect(demoRobotCredentials);
    };
  
    return (
      <div className="w-full h-screen border border-red-500 flex flex-col items-center justify-start">
        <div className="py-8 md:py-12 lg:py-16">
          <h1 className="font-semibold text-2xl">
            Viam TypeScript / React Dashboard Demo
          </h1>
        </div>
        <div className="border border-gray-700 p-4 flex flex-col space-y-4">
          <div className="">
            <h1 className="font-medium">Robot Overview</h1>
            <div className="">
              <p>{`Name: ${demo_robot.name}`}</p>
            </div>
          </div>
          <button
            onClick={handleConnectButton}
            className="px-4 py-2 bg-orange-500 rounded-md font-semibold text-white"
          >
            {status == "loading"
              ? "Loading..."
              : status == "connected"
              ? "Disconnect"
              : "Connect"}
          </button>
        </div>
        {streamClient && (
          <div className="">
            <VideoStream streamClient={streamClient} />
          </div>
        )}
        <div className=""></div>
      </div>
    );
  };
  
  export default DemoPage;