import { Control, Controller } from "react-hook-form";
import Select from "react-select";

interface Props {
  control: Control;
  name: string;
  values: string[];
  id?: string;
}

const FormSelect = ({ control, name, values, id }: Props) => {
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
          value={options.filter((v) => v.value === value)}
          onChange={(v) => onChange((v as any).value)}
          onBlur={onBlur}
        />
      )}
    />
  );
};

export default FormSelect;
