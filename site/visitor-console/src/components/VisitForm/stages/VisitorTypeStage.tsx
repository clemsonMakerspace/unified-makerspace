import React from "react";
import PageCard from "../../PageCard";
import { FormStageProps } from "../types";

const VisitorTypeStage = ({ data, finalize, location }: FormStageProps) => {
  const select_student = () => finalize({ type: "student" });
  const select_guest = () => finalize({ type: "guest" });

  return (
    <PageCard title="Makerspace Sign-In" subtitle={`at ${location.name}`}>
      <div>
        <button
          className="btn-lg btn-secondary mb-3 d-block"
          style={{ width: "250px" }}
          onClick={select_student}
        >
          Clemson User
        </button>

        <button
          className="btn-lg btn-accent d-block"
          style={{ width: "250px" }}
          onClick={select_guest}
        >
          Guest User
        </button>
      </div>
    </PageCard>
  );
};

export default VisitorTypeStage;
