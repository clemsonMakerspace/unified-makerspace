import { useState, useEffect } from "react";
import { Modal, Button } from "react-bootstrap";

interface EquipmentLog {
  user_id: string;
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

interface EditModalProps {
  show: boolean;
  handleClose: () => void;
  log: EquipmentLog | null;
  handleSave: (updatedLog: EquipmentLog) => void;
}

const EditModal = ({ show, handleClose, log, handleSave }: EditModalProps) => {
  const [printStatus, setPrintStatus] = useState<string>("");
  const [printNotes, setPrintNotes] = useState<string>("");

  const is3DPrinter =
    log?.equipment_type === "FDM 3D Printer (Plastic)" ||
    log?.equipment_type === "SLA 3D Printer (Resin)";

  useEffect(() => {
    if (log && is3DPrinter) {
      setPrintStatus(log.print_status || "");
      setPrintNotes(log.print_notes || "");
    }
  }, [log, is3DPrinter]);

  const handleSaveClick = () => {
    if (log) {
      const updatedLog = {
        ...log,
        ...(is3DPrinter && {
          print_status: printStatus,
          print_notes: printNotes,
        }),
      };
      handleSave(updatedLog);
      handleClose();
    }
  };

  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Edit Equipment Log</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {log ? (
          <>
            {Object.entries(log).map(([key, value]) => {
              if (
                key === "print_status" ||
                key === "print_notes" ||
                key === "_ignore" ||
                value === undefined ||
                value === null
              ) {
                return null;
              }

              if (typeof value === "object") {
                // Handle nested objects
                return (
                  <div className="mb-2" key={key}>
                    <strong>{key}:</strong>
                    <ul>
                      {Object.entries(value).map(([nestedKey, nestedValue]) => (
                        <li key={nestedKey}>
                          {nestedKey}: {nestedValue}
                        </li>
                      ))}
                    </ul>
                  </div>
                );
              }

              return (
                <div className="mb-2" key={key}>
                  <span>
                    <strong>{key}:</strong> {value}
                  </span>
                </div>
              );
            })}

            {/* Editable fields only for 3D printers */}
            {is3DPrinter && (
              <>
                <div className="mb-3">
                  <label htmlFor="printStatus" className="form-label">
                    Print Status:
                  </label>
                  <select
                    className="form-control"
                    id="printStatus"
                    value={printStatus}
                    onChange={(e) => setPrintStatus(e.target.value)}
                  >
                    <option value="in progress">In Progress</option>
                    <option value="complete">Complete</option>
                    <option value="failed">Failed</option>
                  </select>
                </div>
                <div className="mb-3">
                  <label htmlFor="printNotes" className="form-label">
                    Print Notes:
                  </label>
                  <textarea
                    className="form-control"
                    id="printNotes"
                    value={printNotes}
                    onChange={(e) => setPrintNotes(e.target.value)}
                  />
                </div>
              </>
            )}
          </>
        ) : (
          <p>No log data available.</p>
        )}
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
        <Button variant="primary" onClick={handleSaveClick}>
          Save Changes
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default EditModal;
