import { ReactNode } from "react";
import Footer from "./Footer";

interface Props {
  title?: string;
  subtitle?: string;
  children?: ReactNode;
}

const PageCard = ({ title, subtitle, children }: Props) => {
  return (
    <div
      className="container bg-primary p-5 rounded d-flex flex-column"
      style={{ minHeight: "27rem", maxWidth: "50rem" }}
    >
      <div className="mb-4 text-center">
        <h1 className="text-secondary fw-bold mb-1">
          {title || "TITLE GOES HERE"}
        </h1>
        {!!subtitle && (
          // <h2 className="text-white text-center fs-3">{subtitle}</h2>
          <span className="text-light fw-bold fs-4">{subtitle}</span>
        )}
      </div>
      <div className="d-flex justify-content-center text-white">{children}</div>
      <div className="flex-grow-1"></div>
      <Footer />
    </div>
  );
};

export default PageCard;
