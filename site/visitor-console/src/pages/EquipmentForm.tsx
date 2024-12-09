import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { api_endpoint } from "../library/constants";

import PageCard from "../components/PageCard";
import { equipmentTypes, projectTypes } from "../library/constants";

import InitialInfo from "../components/EquipmentFormStages/InitialInfo";
import ProjectDetails from "../components/EquipmentFormStages/ProjectDetails";
import Survey from "../components/EquipmentFormStages/Survey";

interface Schema {
  username: string;
  timestamp: string;
  location: string;
  equipment_type: string;
  equipment_history: string;
  project_name: string;
  project_type: string;
  project_details?: string;
  department?: string;
  class_number?: string;
  faculty_name?: string;
  project_sponsor?: string;
  organization_affiliation?: string;
  printer_name?: string;
  print_name?: string;
  print_duration?: string;
  print_mass?: string;
  print_mass_estimate?: string;
  resin_volume?: string;
  resin_type?: string;
  print_status?: string;
  print_notes?: string;
  intern?: string;
  satisfaction?: string;
  difficulties?: string;
  issue_description?: string;
}

const stageSchemas = [
  // First stage - Initial Info
  yup.object({
    username: yup.string().required(),
    location: yup.string().required(),
    equipment_type: yup.string().oneOf(equipmentTypes).required(),
    equipment_history: yup.string().required(),

    // Printer fields with conditional validation
    printer_name: yup.string().when("equipment_type", {
      is: (value: string) =>
        value === "FDM 3D Printer (Plastic)" ||
        value === "SLA 3D Printer (Resin)",
      then: yup.string().required(),
    }),
    print_name: yup.string(),
    print_mass: yup.string().when("equipment_type", {
      is: "FDM 3D Printer (Plastic)",
      then: yup.string().required(),
    }),
    resin_volume: yup.string().when("equipment_type", {
      is: "SLA 3D Printer (Resin)",
      then: yup.string().required(),
    }),
    resin_type: yup.string().when("equipment_type", {
      is: "SLA 3D Printer (Resin)",
      then: yup.string().required(),
    }),
    print_duration: yup.string().when("equipment_type", {
      is: (value: string) =>
        value === "FDM 3D Printer (Plastic)" ||
        value === "SLA 3D Printer (Resin)",
      then: yup.string().required(),
    }),
  }),

  // Second stage - Project Details
  yup.object({
    project_name: yup.string().required(),
    project_type: yup.string().oneOf(projectTypes).required(),
    project_details: yup.string(),
    department: yup.string(),
    class_number: yup.string().when("project_type", {
      is: "Class",
      then: yup
        .string()
        .matches(/^[A-Z]{4}-[0-9]{4}$/, "Invalid class number format")
        .required(),
    }),
    faculty_name: yup.string().when("project_type", {
      is: "Class",
      then: yup.string().required(),
    }),
    project_sponsor: yup.string().when("project_type", {
      is: "Class",
      then: yup.string().required(),
    }),
    organization_affiliation: yup.string().when("project_type", {
      is: "Club",
      then: yup.string().required(),
    }),
  }),

  // Final stage - Survey
  yup.object({
    intern: yup.string().required(),
    satisfaction: yup.string().required(),
    difficulties: yup.string().required(),
    issue_description: yup.string(),
  }),
];

const EquipmentForm = () => {
  const navigate = useNavigate();
  const [saved, setSaved] = useState(false);
  const [stage, setStage] = useState(0);
  const [formData, setFormData] = useState<Partial<Schema>>({});

  const currentSchema = stageSchemas[stage];
  type FormData = yup.InferType<typeof currentSchema>;

  const {
    register,
    handleSubmit,
    control,
    reset,
    watch,
    formState: { errors },
  } = useForm<FormData>({
    resolver: yupResolver(currentSchema),
    mode: "onChange",
    defaultValues: formData as FormData,
  });

  const onSubmit = handleSubmit((data) => {
    setFormData((prevData) => ({ ...prevData, ...data }));

    if (stage < stageComponents.length - 1) {
      setStage((prevStage) => prevStage + 1);
    } else {
      log_equipment({ ...formData, ...data } as Schema);
    }
  });

  const log_equipment = async (form_data: Schema): Promise<void> => {
    // Add print status and notes defaults to form data
    const printerTypes = ["FDM 3D Printer (Plastic)", "SLA 3D Printer (Resin)"];
    const dataWithDefaults = {
      ...form_data,
      ...(printerTypes.includes(form_data.equipment_type) && {
        print_status: form_data.print_status || "In Progress",
        print_notes: form_data.print_notes || "",
      }),
    };
    console.log("Form Submission:", JSON.stringify(dataWithDefaults, null, 2));

    try {
      const response = await fetch(`${api_endpoint}/equipment`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form_data),
      });

      if (response.ok) {
        console.log(
          "Data successfully sent to the API:",
          await response.json()
        );
        setSaved(true);
      } else {
        console.error(
          "Failed to send data to the API:",
          response.status,
          await response.text()
        );
        console.log("Failed to submit the form.");
      }
    } catch (error) {
      console.error("An error occurred while submitting the form:", error);
    }
  };

  if (saved) {
    navigate("/");
  }

  const stageComponents = [
    <InitialInfo
      key={0}
      register={register}
      errors={errors}
      control={control}
      watch={watch}
    />,
    <ProjectDetails
      key={1}
      register={register}
      errors={errors}
      control={control}
      watch={watch}
    />,
    <Survey key={2} register={register} errors={errors} control={control} />,
  ];

  return (
    <PageCard
      title="Equipment use form"
      subtitle="Please Fill in Equipment Information"
    >
      <div className="d-flex flex-column align-items-center text-light">
        <form className="row" onSubmit={onSubmit} style={{ maxWidth: "30rem" }}>
          {stageComponents[stage]}

          {/* Navigation buttons */}
          <div className="d-flex justify-content-between mt-4">
            {stage > 0 ? (
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => {
                  setStage((prevStage) => prevStage - 1);
                  reset(formData as FormData);
                }}
              >
                Back
              </button>
            ) : (
              <Link to="/">
                <button className="btn btn-link text-light" type="button">
                  Cancel
                </button>
              </Link>
            )}
            <button type="submit" className="btn btn-secondary">
              {stage < stageComponents.length - 1 ? "Next" : "Submit"}
            </button>
          </div>
        </form>
      </div>
    </PageCard>
  );
};

export default EquipmentForm;
