import React from "react";
import {
  UseFormRegister,
  FieldErrors,
  Control,
  UseFormWatch,
} from "react-hook-form";
import FormSelect from "../FormSelect";
import { equipmentTypes } from "../../library/constants";

import { locations } from "../../library/constants";

interface InitialInfoProps {
  register: UseFormRegister<any>;
  errors: FieldErrors<any>;
  control: Control<any>;
  watch: UseFormWatch<any>;
}

const InitialInfo: React.FC<InitialInfoProps> = ({
  register,
  errors,
  control,
  watch,
}) => {
  const selectedLocation = watch("location");
  const equipmentType = watch("equipment_type");

  const locationNames = locations.map((location) => location.name);

  const getEquipmentForLocation = (locationName: string) => {
    const location = locations.find((loc) => loc.name === locationName);
    return location ? location.tools : [];
  };

  const getPrintersForLocation = (
    locationName: string,
    type: "fdm_printers" | "sla_printers"
  ) => {
    const location = locations.find((loc) => loc.name === locationName);
    return location && location[type] ? location[type] : [];
  };

  const equipment = getEquipmentForLocation(selectedLocation);
  const printers =
    equipmentType === "FDM 3D Printer (Plastic)"
      ? getPrintersForLocation(selectedLocation, "fdm_printers") ?? []
      : equipmentType === "SLA 3D Printer (Resin)"
      ? getPrintersForLocation(selectedLocation, "sla_printers") ?? []
      : [];

  return (
    <>
      {/* Username */}
      <div className="col-12 mb-2">
        <label htmlFor="username" className="form-label">
          Username
        </label>
        <input
          id="username"
          className="form-control"
          type="text"
          placeholder="Enter username here"
          {...register("username")}
        />
        {errors.username && (
          <p className="text-danger">{errors.username.message}</p>
        )}
      </div>

      {/* Location */}
      <div className="col-12 mb-2">
        <label htmlFor="location" className="form-label">
          Location
        </label>
        <FormSelect control={control} name="location" values={locationNames} />
        {errors.location && (
          <p className="text-danger">{errors.location.message}</p>
        )}
      </div>

      {/* Equipment Type */}
      <div className="col-12 mb-2">
        <label htmlFor="equipment_type" className="form-label">
          Equipment Type
        </label>
        <FormSelect
          control={control}
          name="equipment_type"
          values={equipment}
        />
        {errors.equipment_type && (
          <p className="text-danger">{errors.equipment_type.message}</p>
        )}
      </div>

      {/* Equipment History */}
      <div className="col-12 mb-2">
        <label htmlFor="equipment_history" className="form-label">
          Have you used this piece of equipment before?
        </label>
        <FormSelect
          control={control}
          name="equipment_history"
          values={["Yes", "No"]}
        />
        {errors.equipment_history && (
          <p className="text-danger">{errors.equipment_history.message}</p>
        )}
      </div>

      {/* Conditionally Render Printer Fields */}
      {["FDM 3D Printer (Plastic)", "SLA 3D Printer (Resin)"].includes(
        equipmentType
      ) && (
        <>
          {/* Printer Name */}
          <div className="col-12 mb-2">
            <label htmlFor="printer_name" className="form-label">
              Printer Name
            </label>
            <FormSelect
              control={control}
              name="printer_name"
              values={printers}
            />
            {errors.printer_name && (
              <p className="text-danger">{errors.printer_name.message}</p>
            )}
          </div>

          {/* Print Name */}
          <div className="col-12 mb-2">
            <label htmlFor="print_name" className="form-label">
              Print Name
            </label>
            <input
              id="print_name"
              className="form-control"
              type="text"
              placeholder="Enter a name for the print"
              {...register("print_name")}
            />
            {errors.print_name && (
              <p className="text-danger">{errors.print_name.message}</p>
            )}
          </div>

          {/* FDM Printer Specific Fields */}
          {equipmentType === "FDM 3D Printer (Plastic)" && (
            <>
              {/* Print Mass */}
              <div className="col-12 mb-2">
                <label htmlFor="print_mass" className="form-label">
                  Print Mass
                </label>
                <input
                  id="print_mass"
                  className="form-control"
                  type="text"
                  placeholder="Enter print mass"
                  {...register("print_mass")}
                />
                {errors.print_mass && (
                  <p className="text-danger">{errors.print_mass.message}</p>
                )}
              </div>
            </>
          )}

          {/* SLA Printer Specific Fields */}
          {equipmentType === "SLA 3D Printer (Resin)" && (
            <>
              {/* Resin Volume */}
              <div className="col-12 mb-2">
                <label htmlFor="resin_volume" className="form-label">
                  Resin Volume (in mL)
                </label>
                <input
                  id="resin_volume"
                  className="form-control"
                  type="text"
                  placeholder="Enter resin volume"
                  {...register("resin_volume")}
                />
                {errors.resin_volume && (
                  <p className="text-danger">{errors.resin_volume.message}</p>
                )}
              </div>

              {/* Resin Type */}
              <div className="col-12 mb-2">
                <label htmlFor="resin_type" className="form-label">
                  Resin Type
                </label>
                <FormSelect
                  control={control}
                  name="resin_type"
                  values={["Clear", "Grey"]}
                />
                {errors.resin_type && (
                  <p className="text-danger">{errors.resin_type.message}</p>
                )}
              </div>
            </>
          )}

          {/* Print Duration */}
          <div className="col-12 mb-2">
            <label htmlFor="print_duration" className="form-label">
              Print Duration
            </label>
            <input
              id="print_duration"
              className="form-control"
              type="text"
              placeholder="Enter print duration"
              {...register("print_duration")}
            />
            {errors.print_duration && (
              <p className="text-danger">{errors.print_duration.message}</p>
            )}
          </div>
        </>
      )}
    </>
  );
};

export default InitialInfo;
