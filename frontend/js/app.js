import 'regenerator-runtime/runtime';
import axios from 'axios';

const SERVER = "http://127.0.0.1:5000"


const form = document.getElementById('form');
form.onsubmit = submit;

function submit(event) {
    event.preventDefault();
    CerateSVG()
}

function CerateSVG() {
    const coord = document.getElementById("coord").value
    const time = document.getElementById("time").value
    const date = document.getElementById("date").value
    const city = document.getElementById("city").value
    const info = document.getElementById("info").value

    const data = {
        coord: coord,
        time: time,
        date: date,
        city: city,
        info: info,
        name: uuidv4()
    }
    for (const [key, value] of Object.entries(data)) {
        if (value === null || value === "") {
            alert("فیلد ها همگی الزامی هستند...")
            throw new Error("All fields needs to be filled...")
        }
    }

    const svg = document.querySelector("body");
    const image = document.createElement("img");

    axios.post(SERVER + '/starmap', data).then(response => {
        image.src = response.data.path;
        svg.appendChild(image);
    })
}

function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0,
            v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

function isLatitude(lat) {
    return isFinite(lat) && Math.abs(lat) <= 90;
}

function isLongitude(lng) {
    return isFinite(lng) && Math.abs(lng) <= 180;
}