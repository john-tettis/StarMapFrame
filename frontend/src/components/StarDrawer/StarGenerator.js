import React, {useState} from 'react';

import Message from './Message';
import Music from "./Music";
import GeoLocation from "./GeoLocation";
import Customizer from "./Customizer";
import Done from './Done';

export default function StarGenerator(props) {
    const [step, setStep] = useState(0);
    const [geo, setGeo] = useState({
        location: '',
        date: '',
        time: '',
    });
    const [message, setMessage] = useState({
        line1: '',
        line2: '',
        line3: '',
    })
    const [music, setMusic] = useState({
        mp3: '',
        cover: '',
        singer: '',
        name: '',
    })
    const [customize, setCustomize] = useState({
        size: 'A3',
        background: '#212121',
        frame: '#212121',
        dot: true,
        star: true,
        constellation: true,
        constellationText: true
    })

    const [data, setData] = useState({
        "paint": true,
        "geo": {
            "coordinate": '',
            "date": '',
            "time": '',
            "filename": '',
        },
        "text": {
            "line1": {},
            "line2": {},
            "line3": {},
        },
        "music": {},
        "customize": {
            "size": "A3",
            "frame": "#212121",
            "background": "#000000",
            "dot": true,
            "star": true,
            "constellation": true,
            "constellationText": true,
        },
        "filename": props.filename.name
    });

    if (step === 0) {
        return <GeoLocation data={data} setData={setData} setFileUpdate={props.setFileUpdate} filename={props.filename} updateStep={setStep} step={step}
                            geo={geo} setGeo={setGeo}/>
    }
    if (step === 1) {
        return <Message data={data} setData={setData} filename={props.filename} setFileUpdate={props.setFileUpdate} updateStep={setStep} step={step} message={message}
                        setMessage={setMessage}/>
    }
    if (step === 2) {
        return <Music data={data} setData={setData} filename={props.filename} updateStep={setStep} step={step} music={music} setMusic={setMusic}/>
    }
    if (step === 3) {
        return <Customizer data={data} setData={setData} filename={props.filename} updateStep={setStep} step={step} customize={customize}
                           setCustomize={setCustomize}/>
    }
    if (step === 4) {
        return <Done filename={props.filename} updateStep={setStep} step={step}/>
    }
}