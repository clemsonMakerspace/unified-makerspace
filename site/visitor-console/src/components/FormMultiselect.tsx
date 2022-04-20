import { Control, Controller } from "react-hook-form";
import Select from "react-select";

interface Props {
  control: Control;
  name: string;
  values: string[];
  limit?: number;
  id?: string;
}

const FormMultiselect = ({ control, name, values, id, limit }: Props) => {
  // referenced: https://codesandbox.io/s/react-hook-form-react-select-u36uv

  const options = values.map((value) => ({
    label: value,
    value: value,
  }));

  return (
    <Controller
      name={name}
      control={control}
      render={({ field: { value, onChange, onBlur } }) => (
        <Select
          id={id}
          className="text-dark"
          options={options}
          value={options.filter((v) => value?.includes(v.value))}
          onChange={(v) => onChange(v.map((e) => e.value))}
          onBlur={onBlur}
          isOptionDisabled={() => (limit ? value?.length >= limit : false)}
          isMulti
          isSearchable
        />
      )}
    />
  );
};

export default FormMultiselect;
