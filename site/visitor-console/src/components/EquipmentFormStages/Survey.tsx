import React from "react";
import { UseFormRegister, FieldErrors, Control } from "react-hook-form";
import FormSelect from "../FormSelect";

import { surveryScores, surveyIssues } from "../../library/constants";

interface SurveyProps {
  register: UseFormRegister<any>;
  errors: FieldErrors<any>;
  control: Control<any>;
}

const Survey: React.FC<SurveyProps> = ({ register, errors, control }) => {
  return (
    <>
      {/* Survey/Feedback stage */}
      <div className="col-12 mb-2">
        <label htmlFor="intern" className="form-label">
          Which Intern helped you today?
        </label>
        <input
          id="intern"
          className="form-control"
          type="text"
          placeholder="Enter the intern's name"
          {...register("intern")}
        />
        {errors.resin_volume && (
          <p className="text-danger">{errors.resin_volume.message}</p>
        )}
        {errors.intern && (
          <p className="text-danger">{errors.intern.message}</p>
        )}
      </div>
      <div className="col-12 mb-2">
        <label htmlFor="satisfaction" className="form-label">
          How satisfied were you with the help you received from the Makerspace
          staff (1 being not at all, 10 being very satisfied)?
        </label>
        <FormSelect
          control={control}
          name="satisfaction"
          values={surveryScores}
        />
        {errors.satisfaction && (
          <p className="text-danger">{errors.satisfaction.message}</p>
        )}
      </div>
      <div className="col-12 mb-2">
        <label htmlFor="difficulties" className="form-label">
          Did you have any difficulties today?
        </label>
        <FormSelect
          control={control}
          name="difficulties"
          values={surveyIssues}
        />
        {errors.difficulties && (
          <p className="text-danger">{errors.difficulties.message}</p>
        )}
      </div>
      <div className="col-12 mb-2">
        <label htmlFor="issue_description" className="form-label">
          What specific issues did you have?
        </label>
        <input
          id="issue_description"
          className="form-control"
          type="text"
          placeholder="Describe the issue"
          {...register("issue_description")}
        />
        {errors.issue_description && (
          <p className="text-danger">{errors.issue_description.message}</p>
        )}
      </div>
    </>
  );
};

export default Survey;
