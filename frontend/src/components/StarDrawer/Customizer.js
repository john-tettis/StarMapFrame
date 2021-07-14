import React, {useEffect} from "react";
import axios from "axios";

export default function Customizer(props) {
    const handleChange = async (event, name) => {
        if (name === "size") {
            props.setCustomize({
                size: event.target.id,
                frame: props.customize.frame,
                background: props.customize.background,
                dot: props.customize.dot,
                star: props.customize.star,
                constellation: props.customize.constellation,
                constellationText: props.customize.constellationText
            })
        }
        if (name === "frame") {
            props.setCustomize({
                size: props.customize.size,
                frame: event.target.value,
                background: props.customize.background,
                dot: props.customize.dot,
                star: props.customize.star,
                constellation: props.customize.constellation,
                constellationText: props.customize.constellationText
            })
        }
        if (name === "background") {
            props.setCustomize({
                size: props.customize.size,
                frame: props.customize.frame,
                background: event.target.value,
                dot: props.customize.dot,
                star: props.customize.star,
                constellation: props.customize.constellation,
                constellationText: props.customize.constellationText
            })
        }
        if (name === "dot") {
            props.setCustomize({
                size: props.customize.size,
                frame: props.customize.frame,
                background: props.customize.background,
                dot: event.target.checked,
                star: props.customize.star,
                constellation: props.customize.constellation,
                constellationText: props.customize.constellationText
            })
        }
        if (name === "star") {
            props.setCustomize({
                size: props.customize.size,
                frame: props.customize.frame,
                background: props.customize.background,
                dot: props.customize.dot,
                star: event.target.checked,
                constellation: props.customize.constellation,
                constellationText: props.customize.constellationText
            })
        }
        if (name === "constellation") {
            props.setCustomize({
                size: props.customize.size,
                frame: props.customize.frame,
                background: props.customize.background,
                dot: props.customize.dot,
                star: props.customize.star,
                constellation: event.target.checked,
                constellationText: props.customize.constellationText
            })
        }
        if (name === "constellationText") {
            props.setCustomize({
                size: props.customize.size,
                frame: props.customize.frame,
                background: props.customize.background,
                dot: props.customize.dot,
                star: props.customize.star,
                constellation: props.customize.constellation,
                constellationText: event.target.checked
            })
        }
        await props.setData(state=>{
            state.customize = props.customize;
            if (name==="size") state.customize.size = event.target.id
            if (name==="star") state.customize.star = event.target.checked;
            if (name==="dot") state.customize.dot = event.target.checked;
            if(name==="constellation") state.customize.constellation = event.target.checked;
            if (name==="constellationText") state.customize.constellationText = event.target.checked;
            if(name==="background") state.customize.background = event.target.value;
            if(name==="frame") state.customize.frame = event.target.value;
            return state;
        })
    }

    const sendData = ()=>{
        axios.post("http://localhost:5000/starmap", props.data).then(response=>{
            if (response.status===200 && response.data.result){
                props.setFileUpdate((state) => {
                    state = { name: state.name, isReady: true, hash: Date.now() };
                    return state;
                  });
            }
        }).catch(error=>console.log(error))
    }

    useEffect(() => {
        const timeOutId = setTimeout(() => sendData(), 500);
        return () => clearTimeout(timeOutId);
      }, [props.customize]);
    return (
        <div>
            <h2>حالا قاب خودتو شخصی سازی کن</h2>
            <form onSubmit={event => {
                event.preventDefault();
                props.updateStep(props.step + 1)
            }}>
                <h5>سایز قاب</h5>
                <div onChange={event => handleChange(event, "size")}>
                    <div className="form-check">
                        <input className="form-check-input" type="radio" name="size" id="A2" checked={props.customize.size==="A2"}/>
                        <label className="form-check-label" htmlFor="A2">
                            A2
                        </label>
                    </div>
                    <div className="form-check">
                        <input className="form-check-input" type="radio" name="size" id="A3" defaultChecked={true} checked={props.customize.size==="A3"}/>
                        <label className="form-check-label" htmlFor="A3">
                            A3
                        </label>
                    </div>
                    <div className="form-check">
                        <input className="form-check-input" type="radio" name="size" id="A4" checked={props.customize.size==="A4"}/>
                        <label className="form-check-label" htmlFor="A4">
                            A4
                        </label>
                    </div>
                    <div className="form-check">
                        <input className="form-check-input" type="radio" name="size" id="A5" checked={props.customize.size==="A5"}/>
                        <label className="form-check-label" htmlFor="A5">
                            A5
                        </label>
                    </div>
                </div>
                <hr/>
                <div className="form-group">
                    <label htmlFor="color" className="form-label">انتخاب رنگ قاب</label>
                    <input type="color" className="form-control form-control-color mb-3" id="color"
                           value={props.customize.frame} title="رنگ مورد نظر خود را انتخاب کنید"
                           onChange={event => handleChange(event, "frame")}/>

                </div>
                <div className="form-group">
                    <label htmlFor="background" className="form-label">انتخاب رنگ بکگراند</label>
                    <input type="color" className="form-control form-control-color" id="background"
                           value={props.customize.background} title="رنگ مورد نظر خود را انتخاب کنید"
                           onChange={event => handleChange(event, "background")}/>

                </div>
                <hr/>
                <div className="form-check form-switch">
                    <input className="form-check-input mb-2" type="checkbox" id="dot" defaultChecked={"checked"}
                           onChange={event => handleChange(event, "dot")}/>
                    <label className="form-check-label" htmlFor="dot">نمایش دات</label>
                </div>
                <div className="form-check form-switch">
                    <input className="form-check-input mb-2" type="checkbox" id="star" defaultChecked={"checked"}
                           onChange={event => handleChange(event, "star")}/>
                    <label className="form-check-label" htmlFor="star">نمایش ستاره</label>
                </div>
                <div className="form-check form-switch">
                    <input className="form-check-input mb-2" type="checkbox" id="line" defaultChecked={"checked"}
                           onChange={event => handleChange(event, "constellation")}/>
                    <label className="form-check-label" htmlFor="line">نمایش صور فلکی</label>
                </div>
                <div className="form-check form-switch">
                    <input className="form-check-input" type="checkbox" id="name" checked={!props.customize.constellation ? false: props.customize.constellationText}  defaultChecked={"checked"}
                           onChange={event => handleChange(event, "constellationText")}/>
                    <label className="form-check-label" htmlFor="name">نمایش نام صور فلکی</label>
                </div>
                <div className="row mt-5">
                    <div className="col-6">
                        <button type="button" className="btn btn-outline-danger w-100" onClick={event => {
                            event.preventDefault();
                            props.updateStep(props.step - 1)
                        }}>بازگشت
                        </button>
                    </div>
                    <div className="col-6">
                        <input type="submit" value="ثبت" className="btn btn-primary w-100"/>
                    </div>
                </div>
            </form>
        </div>
    );
}