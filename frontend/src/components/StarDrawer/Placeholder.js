import React from "react";
import frame from "../../assets/img/frame.png";
import "external-svg-loader";
export default class Placeholder extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const SVG_URL = "http://localhost:5000/download/" + this.props.filename.name + "?" + this.props.filename.hash
    return (
      <div id={"star-placeholder"}>
        <img className="img-fluid d-block m-auto" src={frame} alt="Frame" />
        {this.props.filename.isReady ? (
          <svg direction="ltr" data-src={SVG_URL} data-cache="disabled" data-loading="lazy" data-css-scoping="disabled"/>
        ) : (
          ""
        )}
      </div>
    );
  }
}
