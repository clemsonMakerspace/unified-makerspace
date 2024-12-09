import React from "react";
import {
  UseFormRegister,
  FieldErrors,
  Control,
  UseFormWatch,
} from "react-hook-form";
import FormSelect from "../FormSelect";
import { projectTypes } from "../../library/constants";

interface ProjectDetailsProps {
  register: UseFormRegister<any>;
  errors: FieldErrors<any>;
  control: Control<any>;
  watch: UseFormWatch<any>;
}

const ProjectDetails: React.FC<ProjectDetailsProps> = ({
  register,
  errors,
  control,
  watch,
}) => {
  const projectType = watch("project_type");

  return (
    <>
      {/* Project Name */}
      <div className="col-12 mb-2">
        <label htmlFor="project_name" className="form-label">
          What is the name of your project?
        </label>
        <input
          id="project_name"
          className="form-control"
          type="text"
          placeholder="Enter project name"
          {...register("project_name")}
        />
        {errors.project_name && (
          <p className="text-danger">{errors.project_name.message}</p>
        )}
      </div>

      {/* Project Type */}
      <div className="col-12 mb-2">
        <label htmlFor="project_type" className="form-label">
          Project Type
        </label>
        <FormSelect
          control={control}
          name="project_type"
          values={projectTypes}
        />
        {errors.project_type && (
          <p className="text-danger">{errors.project_type.message}</p>
        )}
      </div>

      {/* Research & Creative Inquiry Specific Details */}
      {(projectType === "Research Project" ||
        projectType === "Creative Inquiry") && (
        <>
          <div className="col-12 mb-2">
            <label htmlFor="class_number" className="form-label">
              Project details
            </label>
            <input
              id="class_number"
              className="form-control"
              type="text"
              placeholder="Enter project name"
              {...register("class_number")}
            />
          </div>
          <div className="col-12 mb-2">
            <label htmlFor="class_number" className="form-label">
              What is your department?
            </label>
            <input
              id="class_number"
              className="form-control"
              type="text"
              placeholder="Enter project name"
              {...register("class_number")}
            />
          </div>
        </>
      )}

      {/* Class Project Specific Details */}
      {projectType === "Class Assignment" && (
        <>
          <div className="col-12 mb-2">
            <label htmlFor="class_number" className="form-label">
              What class is this project for?
            </label>
            <input
              id="class_number"
              className="form-control"
              type="text"
              placeholder="Enter class code (e.g., ABCD-1234)"
              {...register("class_number")}
            />
            {errors.class_number && (
              <p className="text-danger">{errors.class_number.message}</p>
            )}
          </div>
          <div className="col-12 mb-2">
            <label htmlFor="faculty_name" className="form-label">
              Who is your professor?
            </label>
            <input
              id="faculty_name"
              className="form-control"
              type="text"
              placeholder="Please enter as First Last"
              {...register("faculty_name")}
            />
            {errors.faculty_name && (
              <p className="text-danger">{errors.faculty_name.message}</p>
            )}
          </div>
        </>
      )}

      {/* Senior Design Specific Details */}
      {projectType === "Senior Design" && (
        <>
          <div className="col-12 mb-2">
            <label htmlFor="faculty_name" className="form-label">
              Who is your advisor for the project?
            </label>
            <input
              id="faculty_name"
              className="form-control"
              type="text"
              placeholder="Enter name as First Last"
              {...register("faculty_name")}
            />
          </div>
          <div className="col-12 mb-2">
            <label htmlFor="project_sponsor" className="form-label">
              Who is the project sponsor?
            </label>
            <input
              id="project_sponsor"
              className="form-control"
              type="text"
              placeholder="Enter company, department or organization"
              {...register("project_sponsor")}
            />
          </div>
        </>
      )}

      {/* Club Specific Details */}
      {projectType === "Club/Organization" && (
        <>
          <div className="col-12 mb-2">
            <label htmlFor="organization_affiliation" className="form-label">
              Organization Affiliation
            </label>
            <input
              id="organization_affiliation"
              className="form-control"
              type="text"
              placeholder="Enter organization affiliation"
              {...register("organization_affiliation")}
            />
            {errors.organization_affiliation && (
              <p className="text-danger">
                {errors.organization_affiliation.message}
              </p>
            )}
          </div>
        </>
      )}
    </>
  );
};

export default ProjectDetails;
