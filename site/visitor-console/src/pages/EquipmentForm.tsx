import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { api_endpoint } from "../library/constants";

import PageCard from "../components/PageCard";
import { projectTypes } from "../library/constants";

import InitialInfo from "../components/EquipmentFormStages/InitialInfo";
import ProjectDetails from "../components/EquipmentFormStages/ProjectDetails";
import Survey from "../components/EquipmentFormStages/Survey";

import { EquipmentSchema } from "../library/types";

import {
  FDM_PRINTER_STRING,
  SLA_PRINTER_STRING,
  is3DPrinter,
} from "../library/constants";

const stageSchemas = [
  // First stage - Initial Info
  yup.object({
    user_id: yup.string().required(),
    location: yup.string().required(),
    equipment_type: yup.string().required(),
    equipment_history: yup.string().required(),

    // Printer fields with conditional validation
    printer_3d_info: yup
      .object()
      .shape({
        printer_name: yup.string().required(),
        print_name: yup.string().required(),
        print_duration: yup.string().required(),
        print_status: yup.string().default("In Progress"),
        print_notes: yup.string().default(""),

        // Specifically require estimated print mass when using plastic 3d printers
        print_mass_estimate: yup.string().when("equipment_type", {
          is: FDM_PRINTER_STRING,
          then: yup.string().required(),
          otherwise: yup.string().notRequired(),
        }),

        // Specifically require resin volume and type when using resin 3d printers
        resin_volume: yup.string().when("equipment_type", {
          is: SLA_PRINTER_STRING,
          then: yup.string().required(),
          otherwise: yup.string().notRequired(),
        }),
        resin_type: yup.string().when("equipment_type", {
          is: SLA_PRINTER_STRING,
          then: yup.string().required(),
          otherwise: yup.string().notRequired(),
        }),
      })
      .when("equipment_type", {
        // .when() here is for printer_3d_info
        is: is3DPrinter,
        then: yup.object().required(),
        otherwise: yup.object().notRequired(),
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
  const [formData, setFormData] = useState<Partial<EquipmentSchema>>({});

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
      post_equipment_form({ ...formData, ...data } as EquipmentSchema);
    }
  });

  const post_equipment_form = async (
    form_data: EquipmentSchema
  ): Promise<void> => {
    // Add print status and notes defaults to form data
    const dataWithDefaults = {
      ...form_data,
      timestamp: new Date().toISOString().split(".")[0],
    };
    console.log("Form Submission:", JSON.stringify(dataWithDefaults, null, 2));

    //try {
    //  const response = await fetch(`${api_endpoint}/equipment`, {
    //    method: "POST",
    //    headers: {
    //      "Content-Type": "application/json",
    //    },
    //    body: JSON.stringify(dataWithDefaults),
    //  });

    //  if (response.ok) {
    //    console.log(
    //      "Data successfully sent to the API:",
    //      await response.json()
    //    );
    //    setSaved(true);
    //  } else {
    //    console.error(
    //      "Failed to send data to the API:",
    //      response.status,
    //      await response.text()
    //    );
    //    console.log("Failed to submit the form.");
    //  }
    //} catch (error) {
    //  console.error("An error occurred while submitting the form:", error);
    //}
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
