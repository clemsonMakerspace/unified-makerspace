import React from "react";
import PageCard from "../../PageCard";
import { FormStageProps } from "../types";

const ToolSurveyStage = ({ data, finalize, location }: FormStageProps) => {
  const { tools } = location;

  // if there are no tools then skip this stage
  if (tools.length === 0) finalize(data);

  const select_tool = (tool: string) => () => finalize({ ...data, tool });

  return (
    <PageCard
      title="Tool Survey"
      subtitle="What tool will you use the most today?"
    >
      <div className="d-flex gap-3 flex-wrap justify-content-center">
        {location.tools.map((tool, i) => (
          <button
            className="btn btn-secondary"
            key={i}
            onClick={select_tool(tool)}
          >
            {tool}
          </button>
        ))}
      </div>
    </PageCard>
  );
};

export default ToolSurveyStage;
