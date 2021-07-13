import React, {useState} from 'react';
import moment from 'moment-jalali';
import axios from "axios";

import DatePicker from "react-multi-date-picker";
import TimePicker from 'rc-time-picker';
import 'rc-time-picker/assets/index.css';

import {Client} from "@googlemaps/google-maps-services-js";

const API_KEY = "AIzaSyBgBc9WzvrQY4A2AJNrahd1Od8LRI2lv9w";

export default function GeoLocation(props) {
    const [dateValue, setDateValue] = useState(new Date());

    let geo = {
        location: '',
        date: dateValue,
        time: ''
    }
    // Time Picker Config
    const format = 'HH.mm.ss';
    const handleTimeChange = (value) => {
        geo.time = value && value.format(format);
    }
    const handleDateChange = (date, format = "YYYY/MM/DD") => {
        setDateValue(date);
    }

    const client = new Client({});
    const googleGeoCoder = () => {
        client.geocode({
            params: {
                address: geo.location.value,
                key: API_KEY
            }
        }).then(r => {
            geo.location = r.data.results[0].geometry.location
            props.setData(state=>{
                state.geo = geo;
                state.geo.date = `${dateValue.unix}`
                return state
            })
            console.log(props.data)
            axios.post("http://127.0.0.1:5000/starmap", props.data).then(response => {
                if (response.status === 200 && response.data.result) {
                    props.updateStep(props.step + 1)
                }
            }).catch(error => console.log(error))
        }).catch(e => {
            console.log(e)
        })
    }
    const geoCodeSuggest = () => {
        client.placeAutocomplete({
            params: {
                input: geo.location.value,
                key: API_KEY
            }
        }).then(r => {
            const opt = document.getElementById("datalistOptions")
            opt.innerHTML = '';
            r.data.predictions.forEach(item => {
                const child = document.createElement("option");
                child.setAttribute("value", item.description);
                opt.appendChild(child);
            })
        }).catch(e => {
            console.log(e)
        })
    }

    // noinspection CheckTagEmptyBody
    return (
        <div>
            <h2>ابتدا مناسبت را مشخص نمایید...</h2>
            <form onSubmit={event => {
                    event.preventDefault();
                    props.setGeo({location: geo.location.value, date: dateValue, time: geo.time});
                    googleGeoCoder();
                    props.fileUpdated({name: props.filename.name, isReady: true});
                }
            }>
                <div className="form-group mb-3">
                    <label htmlFor="location">موقعیت مکانی</label>
                    <input className="form-control" list="datalistOptions" id="location" autoComplete="off"
                           ref={el => geo.location = el} onChange={event => geoCodeSuggest()}/>
                    <datalist id="datalistOptions"></datalist>
                </div>
                <div className="form-group mb-3">
                    <label htmlFor="date">تاریخ</label>
                    <DatePicker value={dateValue} onChange={handleDateChange}
                                inputClass="form-control" locale={"fa"}
                                calendar={"persian"} type={"input-icon"} calendarPosition="auto-right"
                                format={"YYYY/MM/DD"}/>
                </div>
                <div className="form-group">
                    <label htmlFor="time">ساعت</label>
                    <TimePicker
                        showSecond={false}
                        defaultValue={moment()}
                        className="time-picker-control"
                        onChange={handleTimeChange}
                    />
                </div>
                <input type="submit" value="ثبت" className="btn btn-primary mt-5 w-100"/>
            </form>
        </div>
    )
}