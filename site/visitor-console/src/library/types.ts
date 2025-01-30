export interface MakerspaceLocation {
  slug: string;
  name: string;
  tools: string[];
}

export interface Printer3DInfo {
  printer_name: string;
  print_name: string;
  print_duration: string;
  print_status: string;
  print_notes: string;
  print_mass?: string;
  print_mass_estimate?: string;
  resin_volume?: string;
  resin_type?: string;
}

export interface EquipmentSchema {
  user_id: string;
  timestamp: string;
  location: string;
  equipment_type: string;
  equipment_history: string;
  project_name: string;
  project_type: string;
  project_details?: string;
  printer_3d_info?: Printer3DInfo;
  department?: string;
  class_number?: string;
  faculty_name?: string;
  project_sponsor?: string;
  organization_affiliation?: string;
  printer_name?: string;
  resin_volume?: string;
  resin_type?: string;
  intern?: string;
  satisfaction?: string;
  difficulties?: string;
  issue_description?: string;
}

export interface EquipmentLog extends EquipmentSchema {
  _ignore?: string;
}
