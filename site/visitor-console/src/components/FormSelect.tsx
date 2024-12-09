import { Control, Controller, Path, FieldValues } from "react-hook-form";
import Select from "react-select";

interface OptionType {
  label: string;
  value: string;
}

interface Props<TFieldValues extends FieldValues> {
  control: Control<TFieldValues>;
  name: Path<TFieldValues>;
  values: string[];
  id?: string;
}

const FormSelect = <TFieldValues extends FieldValues>({
  control,
  name,
  values,
  id,
}: Props<TFieldValues>) => {
  const options: OptionType[] = values.map((value) => ({
    label: value,
    value: value,
  }));

  return (
    <Controller
      name={name}
      control={control}
      render={({ field }) => (
        <Select
          id={id}
          className="text-dark"
          options={options}
          value={options.find((option) => option.value === field.value)}
          onChange={(option) => field.onChange(option ? option.value : "")}
          onBlur={field.onBlur}
        />
      )}
    />
  );
};

export default FormSelect;
