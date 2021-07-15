import React, { useEffect } from "react";
import axios from "axios";

export default function Message(props) {
  const handleChange = (event, name) => {
    if (name === "line1") {
      props.setMessage({
        line1: {
          value: event.target.value,
          size: props.message.line1.size,
          font: props.message.line1.font
        },
        line2: props.message.line2,
        line3: props.message.line3,
      });
    }
    if (name === "line2") {
      props.setMessage({
        line1: props.message.line1,
        line2: {
          value: event.target.value,
          size: props.message.line2.size,
          font: props.message.line2.font
        },
        line3: props.message.line3,
      });
    }
    if (name === "line3") {
      props.setMessage({
        line1: props.message.line1,
        line2: props.message.line2,
        line3: {
          value: event.target.value,
          size: props.message.line3.size,
          font: props.message.line3.font
        },
      });
    }
    props.setData((state) => {
      if (name === "line1") state.text.line1.value = event.target.value;
      if (name === "line1-font") state.text.line1.font = event.target.value;
      if (name === "line1-size") state.text.line1.size = event.target.value;

      if (name === "line2") state.text.line2.value = event.target.value;
      if (name === "line2-font") state.text.line2.font = event.target.value;
      if (name === "line2-size") state.text.line2.size = event.target.value;
      

      if (name === "line3") state.text.line3.value = event.target.value;
      if (name === "line3-font") state.text.line3.font = event.target.value;
      if (name === "line3-size") state.text.line3.size = event.target.value;

      return state;
    });
  };

  const sendData = () => {
    axios.post("http://localhost:5000/starmap", props.data).then((response) => {
      if (response.status === 200 && response.data.result) {
        props.setFileUpdate((state) => {
          state = { name: state.name, isReady: true, hash: Date.now() };
          return state;
        });
      }
    });
  };
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
          props.updateStep(props.step + 1);
        }}
      >
        <div className="form-group mb-5">
          <label htmlFor="message">خط اول</label>
          <input
            className="form-control mb-3"
            type="text"
            name="line1"
            id="line1"
            value={props.message.line1.value}
            onChange={(event) => handleChange(event, "line1")}
            autoFocus
            placeholder="متن دلخواه خود را تایپ کنید.."
          />
          <label htmlFor="line1-font">فونت</label>
          <select
            onChange={(event) => handleChange(event, "line1-font")}
            dir="ltr"
            className="form-select"
            name="line1-font"
            id="line1-font"
          >
            <option value="Anton" selected>
              Anton
            </option>
            <option value="Dancing Script">Dancing Script</option>
            <option value="Fuggles">Fuggles</option>
            <option value="Karla">Karla</option>
            <option value="Qahiri">Qahiri</option>
            <option value="Roboto">Roboto</option>
            <option value="Roboto Slab">Roboto Slab</option>

            <option value="Kamran">کامران</option>
            <option value="Mikhak">میهک</option>
            <option value="Yekan">یکان</option>

          </select>
          <label htmlFor="line1-size">سایز فونت</label>
          <input
            className="form-control"
            type="number"
            id="line1-size"
            name="line1-size"
            value={props.message.line1.size}
            onChange={(event) => handleChange(event, "line1-size")}
          />
        </div>

        <div className="form-group mb-5">
          <label htmlFor="message">خط دوم</label>
          <input
            className="form-control mb-3"
            type="text"
            name="line2"
            id="line2"
            value={props.message.line2.value}
            onChange={(event) => handleChange(event, "line2")}
          />

          <label htmlFor="line1-font">فونت</label>
          <select
            onChange={(event) => handleChange(event, "line2-font")}
            dir="ltr"
            className="form-select"
            name="line2-font"
            id="line2-font"
          >
            <option value="Anton" selected>
              Anton
            </option>
            <option value="Dancing Script">Dancing Script</option>
            <option value="Fuggles">Fuggles</option>
            <option value="Karla">Karla</option>
            <option value="Qahiri">Qahiri</option>
            <option value="Roboto">Roboto</option>
            <option value="Roboto Slab">Roboto Slab</option>

            <option value="Kamran">کامران</option>
            <option value="Mikhak">میهک</option>
            <option value="Yekan">یکان</option>
          </select>

          <label htmlFor="line2-size">سایز فونت</label>
          <input
            className="form-control"
            type="number"
            id="line2-size"
            name="line2-size"
            value={props.message.line2.size}
            onChange={(event) => handleChange(event, "line2-size")}
          />
        </div>

        <div className="form-group mb-5">
          <label htmlFor="message">خط سوم</label>
          <input
            className="form-control"
            type="text"
            name="line3"
            id="line3"
            value={props.message.line3.value}
            onChange={(event) => handleChange(event, "line3")}
          />
          <label htmlFor="line1-font">فونت</label>
          <select
            onChange={(event) => handleChange(event, "line3-font")}
            dir="ltr"
            className="form-select"
            name="line3-font"
            id="line3-font"
          >
            <option value="Anton" selected>
              Anton
            </option>
            <option value="Dancing Script">Dancing Script</option>
            <option value="Fuggles">Fuggles</option>
            <option value="Karla">Karla</option>
            <option value="Qahiri">Qahiri</option>
            <option value="Roboto">Roboto</option>
            <option value="Roboto Slab">Roboto Slab</option>

            <option value="Kamran">کامران</option>
            <option value="Mikhak">میهک</option>
            <option value="Yekan">یکان</option>
          </select>
          <label htmlFor="line3-size">سایز فونت</label>
          <input
            className="form-control"
            type="number"
            id="line3-size"
            name="line3-size"
            value={props.message.line3.size}
            onChange={(event) => handleChange(event, "line3-size")}
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
