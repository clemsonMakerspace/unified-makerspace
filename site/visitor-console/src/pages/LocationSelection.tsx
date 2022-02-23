import { Link } from "react-router-dom";

import PageCard from "../components/PageCard";
import { locations } from "../library/constants";

const LocationSelection = () => {
  return (
    <PageCard title="Makerspace Sign-In" subtitle="Location Selection">
      <div className="d-flex gap-3">
        {locations.map(({ slug, name }) => (
          <Link to={`/${slug}`} key={slug}>
            <button className="btn btn-secondary">{name}</button>
          </Link>
        ))}
      </div>
    </PageCard>
  );
};

export default LocationSelection;
