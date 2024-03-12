import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { MakerspaceLocation } from "../../library/types";
import { FormData } from "./types";

import VisitorTypeStage from "./stages/VisitorTypeStage";
import UsernameStage from "./stages/UsernameStage";
import ToolSurveyStage from "./stages/ToolSurveyStage";
import PageCard from "../PageCard";
import { api_endpoint } from "../../library/constants";

const stages = [VisitorTypeStage, UsernameStage, ToolSurveyStage];

interface VisitFormProps {
  location: MakerspaceLocation;
}

const VisitForm = ({ location }: VisitFormProps) => {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<Partial<FormData>>({});
  const [stage, setStage] = useState<number>(0);

  const finalize = (new_data: Partial<FormData>) => {
    // update the data
    setData(new_data);

    // submit data on last stage
    if (stage === stages.length - 1) submit_data(new_data as FormData);
    // otherwise increment the stage pointer
    else setStage((stage) => stage! + 1);
  };

  const submit_data = (data: FormData) => {
    const body = {
      username: data.username,
      location: location.name,
      tool: data.tool,
    };

    setLoading(true);
    fetch(`${api_endpoint}/visit`, {
      method: "post",
      body: JSON.stringify(body),
    }).then((response) => {
      setLoading(false);
      if (response.ok) {
        navigate(`/success?next=/${location.slug}&username=${data.username}`);
      } else {
        navigate(`/error?next=/${location.slug}`);
      }
    });
  };

  const reset = () => {
    setData({});
    setStage(0);
  };

  const Stage = stages[stage];

  if (loading)
    return <PageCard title="Sign-in" subtitle="Loading..."></PageCard>;

  return <Stage {...{ data, finalize, location, reset }} />;
};

export default VisitForm;
