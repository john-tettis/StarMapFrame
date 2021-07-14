import React, { useEffect } from "react";
import axios from "axios";

export default function Message(props) {
  const handleChange = (event, name) => {
    if (name === "line1") {
      props.setMessage({
        line1: event.target.value,
        line2: props.message.line2,
        line3: props.message.line3,
      });
    }
    if (name === "line2") {
      props.setMessage({
        line1: props.message.line1,
        line2: event.target.value,
        line3: props.message.line3,
      });
    }
    if (name === "line3") {
      props.setMessage({
        line1: props.message.line1,
        line2: props.message.line2,
        line3: event.target.value,
      });
    }
    props.setData((state) => {
      if (name === "line1") state.text.line1 = event.target.value;
      if (name === "line2") state.text.line2 = event.target.value;
      if (name === "line3") state.text.line3 = event.target.value;
      return state;
    });
  };
  
  const sendData = ()=>{
    axios
    .post("http://localhost:5000/starmap", props.data)
    .then((response) => {
      if (response.status === 200 && response.data.result) {
        props.setFileUpdate((state) => {
          state = { name: state.name, isReady: true, hash: Date.now() };
          return state;
        });
      }
    });
  }
  useEffect(() => {
    const timeOutId = setTimeout(() => sendData(), 500);
    return () => clearTimeout(timeOutId);
  }, [props.message]);

  return (
    <div>
      <h2>حالا متن دلخواه خود را بنویسید</h2>
      <form
        onSubmit={(event) => {
          event.preventDefault();
          props.setMessage({
            line1: props.message.line1,
            line2: props.message.line2,
            line3: props.message.line3,
          });
          props.updateStep(props.step + 1);
        }}
      >
        <div className="form-group">
          <label htmlFor="message">خط اول</label>
          <input
            className="form-control mb-3"
            type="text"
            name="line1"
            id="line1"
            value={props.message.line1}
            onChange={(event) => handleChange(event, "line1")}
            autoFocus
          />
        </div>
        <div className="form-group">
          <label htmlFor="message">خط دوم</label>
          <input
            className="form-control mb-3"
            type="text"
            name="line2"
            id="line2"
            value={props.message.line2}
            onChange={(event) => handleChange(event, "line2")}
          />
        </div>
        <div className="form-group">
          <label htmlFor="message">خط سوم</label>
          <input
            className="form-control"
            type="text"
            name="line3"
            id="line3"
            value={props.message.line3}
            onChange={(event) => handleChange(event, "line3")}
          />
        </div>
        <div className="row mt-5">
          <div className="col-6">
            <button
              type="button"
              onClick={(event) => {
                event.preventDefault();
                props.updateStep(props.step - 1);
              }}
              className="btn btn-outline-danger w-100"
            >
              بازگشت
            </button>
          </div>
          <div className="col-6">
            <input
              type="submit"
              value="ثبت"
              className="btn btn-primary w-100"
            />
          </div>
        </div>
      </form>
    </div>
  );
}
