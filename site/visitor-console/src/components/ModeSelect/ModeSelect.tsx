import { Props } from '../App/App';

const ModeSelect = (props: Props) => (
  <div>
      <button className="btn-lg btn-secondary mb-3 d-block" 
      style={{width: '250px'}} 
      onClick={props.handleClemsonUser}>Clemson User</button>
      
      <button className="btn-lg btn-accent mb-3 d-block" 
      style={{width: '250px'}} 
      onClick={props.handleGuestUser}>Guest User</button>
  </div>
);

export default ModeSelect;
