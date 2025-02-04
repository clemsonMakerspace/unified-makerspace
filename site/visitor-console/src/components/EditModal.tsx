import { useState, useEffect } from "react";
import { Modal, Button } from "react-bootstrap";

import { FDM_PRINTER_STRING, SLA_PRINTER_STRING } from "../library/constants";

import { EquipmentLog } from "../library/types";

import { is3DPrinter } from "../library/constants";

interface EditModalProps {
  show: boolean;
  handleClose: () => void;
  log: EquipmentLog | null;
  handleSave: (updatedLog: EquipmentLog) => void;
}

const EditModal = ({ show, handleClose, log, handleSave }: EditModalProps) => {
  const [printStatus, setPrintStatus] = useState<string>("");
  const [printNotes, setPrintNotes] = useState<string>("");
  const [printMass, setPrintMass] = useState<string>("");

  useEffect(() => {
    if (log && is3DPrinter(log?.equipment_type)) {
      setPrintStatus(log?.printer_3d_info?.print_status || "");
      setPrintNotes(log?.printer_3d_info?.print_notes || "");
      setPrintMass(log?.printer_3d_info?.print_mass || "");
    }
  }, [log]);

  const handleSaveClick = () => {
    if (log) {
      const updatedLog = {
        ...log,
        ...(log.printer_3d_info && {
          printer_3d_info: {
            ...log.printer_3d_info,
            print_status: printStatus,
            print_notes: printNotes,
            print_mass: printMass,
          },
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
              if (key === "_ignore" || value === undefined || value === null) {
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
            {is3DPrinter(log.equipment_type) && (
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
                    <option value="In Progress">In Progress</option>
                    <option value="Complete">Complete</option>
                    <option value="Failed">Failed</option>
                  </select>
                </div>
                <div className="mb-3">
                  <label htmlFor="printMass" className="form-label">
                    Print Mass:
                  </label>
                  <textarea
                    className="form-control"
                    id="printMass"
                    value={printMass}
                    onChange={(e) => setPrintMass(e.target.value)}
                  />
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
