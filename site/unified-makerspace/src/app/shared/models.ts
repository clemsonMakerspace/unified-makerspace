export interface Request {
  requester_name: string;
  request_id: string;
  description: string;
}

export interface Task {
  task_name: string;
  task_id: string;
  description: string;
  assigned_to: string;
  status: string;
}

export interface User {
  first_name: string;
  last_name: string;
  user_id: string;
  hardware_id: string;
  assigned_tasks: [Task];
}

export interface Visitor {
  date_visited: string;
  is_new: boolean;
}
