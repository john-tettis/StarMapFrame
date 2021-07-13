import React from 'react';

export default function Music(props) {
    const handleChange = (event, name) => {
        if (name === "mp3") {
            props.setMusic({
                mp3: event.target.value,
                cover: props.music.cover,
                singer: props.music.singer,
                name: props.music.name
            })
        }
        if(name==="cover"){
            props.setMusic({
                mp3: props.music.mp3,
                cover: event.target.value,
                singer: props.music.singer,
                name: props.music.name
            })
        }
        if(name==="singer"){
            props.setMusic({
                mp3: props.music.mp3,
                cover: props.music.cover,
                singer: event.target.value,
                name: props.music.name
            })
        }
        if(name==="name"){
            props.setMusic({
                mp3: props.music.mp3,
                cover: props.music.cover,
                singer: props.music.singer,
                name: event.target.value
            })
        }
    }
    return (
        <div>
            <h2>میخوای موسیقی‌ای آپلود کنی؟</h2>
            <form onSubmit={event => {
                event.preventDefault();
                props.updateStep(props.step + 1)
            }}>
                <div className="form-group">
                    <label htmlFor="mp3" className="form-label">فایل آهنگ</label>
                    <input type="file" className="form-control mb-3" name="mp3" id="mp3" value={props.music.mp3}
                           onChange={event => handleChange(event, "mp3")}/>
                </div>
                <div className="form-group">
                    <label htmlFor="cover" className="form-label">کاور آهنگ</label>
                    <input type="file" className="form-control mb-3" name="cover" id="cover"
                           value={props.music.cover} onChange={event => handleChange(event, "cover")}/>
                </div>
                <div className="form-group">
                    <label htmlFor="singer">نام خواننده</label>
                    <input className="form-control mb-3" type="text" name="singer" id="singer"
                           value={props.music.singer} onChange={event => handleChange(event, "singer")}/>
                </div>
                <div className="form-group">
                    <label htmlFor="name">نام آهنگ</label>
                    <input className="form-control mb-3" type="text" name="name" id="name" value={props.music.name}
                           onChange={event => handleChange(event, "name")}/>
                </div>
                <div className="row">
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
        </div>)
}