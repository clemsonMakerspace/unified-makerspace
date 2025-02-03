import { useState, useEffect } from "react";
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

// Used for transforming objects before POST to api
const Printer3DInfoKeys = new Set([
  "printer_name",
  "print_name",
  "print_duration",
  "print_status",
  "print_notes",
  "print_mass",
  "print_mass_estimate",
  "resin_volume",
  "resin_type",
]);

const stageSchemas = [
  // First stage - Initial Info
  yup.object({
    user_id: yup.string().required().label("User ID"),
    location: yup.string().required().label("Makerspace Location"),
    equipment_type: yup.string().required().label("Equipment Type"),
    equipment_history: yup.string().required().label("Equipment History"),

    // Printer fields with conditional validation
    // These will be transformed into the appropriate printer_3d_info object
    // before sending the full data object to the api.
    printer_name: yup.string().when("equipment_type", {
      is: is3DPrinter,
      then: yup.string().required().label("Printer Name"),
      otherwise: yup.string().notRequired(),
    }),
    print_name: yup.string().when("equipment_type", {
      is: is3DPrinter,
      then: yup.string().required().label("Print Name"),
      otherwise: yup.string().notRequired(),
    }),
    print_duration: yup.string().when("equipment_type", {
      is: is3DPrinter,
      then: yup.string().required().label("Print Duration"),
      otherwise: yup.string().notRequired(),
    }),
    print_status: yup.string().when("equipment_type", {
      is: is3DPrinter,
      then: yup.string().default("In Progress"),
      otherwise: yup.string().notRequired(),
    }),
    print_notes: yup.string().when("equipment_type", {
      is: is3DPrinter,
      then: yup.string().default(""),
      otherwise: yup.string().notRequired(),
    }),

    // Specifically require estimated print mass when using plastic 3d printers
    print_mass_estimate: yup.string().when("equipment_type", {
      is: FDM_PRINTER_STRING,
      then: yup.string().required().label("Print Mass Estimate"),
      otherwise: yup.string().notRequired(),
    }),

    // Default print mass to the unknown value as the print hasn't finished
    print_mass: yup.string().when("equipment_type", {
      is: FDM_PRINTER_STRING,
      then: (schema) => schema.default(""),
      otherwise: (schema) => schema.notRequired(),
    }),

    // Specifically require resin volume and type when using resin 3d printers
    resin_volume: yup.string().when("equipment_type", {
      is: SLA_PRINTER_STRING,
      then: (schema) => schema.required().label("Resin Volume"),
      otherwise: (schema) => schema.notRequired(),
    }),
    resin_type: yup.string().when("equipment_type", {
      is: SLA_PRINTER_STRING,
      then: (schema) => schema.required().label("Resin Type"),
      otherwise: (schema) => schema.notRequired(),
    }),
  }),

  // Second stage - Project Details
  yup.object({
    project_name: yup.string().required().label("Project Name"),
    project_type: yup
      .string()
      .oneOf(projectTypes)
      .required()
      .label("Project Type"),
    project_details: yup.string(),
    department: yup.string(),
    class_number: yup.string().when("project_type", {
      is: "Class",
      then: yup
        .string()
        .matches(/^[A-Z]{4}-[0-9]{4}$/, "Invalid class number format")
        .required()
        .label("Class Number"),
    }),
    faculty_name: yup.string().when("project_type", {
      is: "Class",
      then: yup.string().required().label("Faculty Name"),
    }),
    project_sponsor: yup.string().when("project_type", {
      is: "Class",
      then: yup.string().required().label("Project Sponsor"),
    }),
    organization_affiliation: yup.string().when("project_type", {
      is: "Club",
      then: yup.string().required().label("Organization Affiliation"),
    }),
  }),

  // Final stage - Survey
  yup.object({
    intern: yup.string(),
    satisfaction: yup.string(),
    difficulties: yup.string(),
    issue_description: yup.string(),
  }),
];

const EquipmentForm = () => {
  const navigate = useNavigate();
  const [stage, setStage] = useState(0);
  const [formData, setFormData] = useState<Partial<EquipmentSchema>>({});

  const currentSchema = stageSchemas[stage] ?? yup.object();
  type FormData = yup.InferType<typeof currentSchema>;

  const {
    register,
    handleSubmit,
    control,
    reset,
    watch,
    setValue,
    formState: { errors },
  } = useForm<FormData>({
    resolver: yupResolver(currentSchema),
    mode: "onChange",
    shouldUnregister: true,
  });

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

  const [stageData, setStageData] = useState(
    new Array(stageComponents.length).fill(null)
  );

  const onSubmit = handleSubmit((data) => {
    console.log(`Submitted data: ${JSON.stringify(data, null, 2)}`);

    setFormData((prevData) => ({ ...prevData, ...data }));

    setStageData((prevData) => {
      const updatedData = [...prevData];
      updatedData[stage] = { ...data };
      return updatedData;
    });

    if (stage < stageComponents.length - 1) {
      setStage((prevStage) => prevStage + 1);
      reset({ ...formData, ...data });
    } else {
      // A bit scuffed having duplicate code, but this is
      // necessary to provide the post request with the
      // latest data.
      setStageData((prevData) => {
        const updatedData = [...prevData];
        updatedData[stage] = { ...data };
        post_equipment_form(updatedData);
        return updatedData;
      });
    }
  });

  const post_equipment_form = async (latestStageData: any[]): Promise<void> => {
    // Compress the array of stage data into one object
    // Note: reduce() works as expected as long as all keys are unique.
    // It overwrites the same keys with the value of the last one evaluated.
    const allStageData = latestStageData.reduce(
      (acc, obj) => ({ ...acc, ...obj }),
      {}
    );

    // Transform data relating to 3d printers into a printer_3d_info object
    const transformedData = Object.keys(allStageData).reduce(
      (acc, key) => {
        //console.log(`Checking key: ${key}`);
        if (Printer3DInfoKeys.has(key)) {
          acc.printer_3d_info[key] = allStageData[key]; // Move to "printer_3d_info"
          console.log(`Adding value: ${allStageData[key]}`);
          console.log(`Acc is now: ${JSON.stringify(acc, null, 2)}`);
        } else {
          acc[key] = allStageData[key]; // Keep other fields
        }
        return acc;
      },
      { printer_3d_info: {} } as Record<string, any>
    );

    // Remove the printer_3d_info key if the equipment_type is not a printer
    // Currently guaranteed to have this field via the attempted transformation
    // from above.
    if (!is3DPrinter(transformedData.equipment_type)) {
      delete transformedData.printer_3d_info;
    }

    // Add the timestamp to the data
    const dataWithDefaults = {
      ...transformedData,
      timestamp: new Date().toISOString().split(".")[0],
    };
    console.log("Form Submission:", JSON.stringify(dataWithDefaults, null, 2));

    try {
      const response = await fetch(`${api_endpoint}/equipment`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dataWithDefaults),
      });

      if (response.ok) {
        console.log(
          "Data successfully sent to the API:",
          await response.json()
        );
        navigate("/");
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
