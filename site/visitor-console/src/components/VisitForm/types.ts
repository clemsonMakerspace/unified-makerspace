import { MakerspaceLocation } from "../../library/types";

type VisitType = "student" | "guest";

export interface FormData {
  type: VisitType;
  username: string;
  tool: string;
}

export interface FormStageProps {
  location: MakerspaceLocation;
  data: Partial<FormData>;
  finalize: (new_data: Partial<FormData>) => void;
  reset: () => void;
}
