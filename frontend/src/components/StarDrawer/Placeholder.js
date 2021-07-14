import React from "react";
import frame from "../../assets/img/frame.png";

export default class Placeholder extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div id={"star-placeholder"}>
        <img className="img-fluid d-block m-auto" src={frame} alt="Frame" />
        {this.props.filename.isReady ? (
          <img
            src={
              "http://localhost:5000/download/" +
              this.props.filename.name +
              "?" +
              this.props.filename.hash
            }
            alt={"star"}
          />
        ) : (
          ""
        )}
      </div>
    );
  }
}
