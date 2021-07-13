import React from "react";


export default function Done(props) {
    return (
        <div>
            <h2>قاب آماده است!</h2>
            <p>حالا می‌تونی با دکمه‌ی ثبت سفارش ٬ سفارش خودتو ثبت کنی یا اگر این مشخصات راضی کننده نیست یه بار دیگه
                امتحان کنی...</p>
            <div className="row">
                <div className="col-6">
                    <button type="button" className="btn btn-outline-danger w-100" onClick={event => {
                        event.preventDefault();
                        props.updateStep(props.step - 4)
                    }}>امتحان دوباره
                    </button>
                </div>
                <div className="col-6">
                    <button type="button" className="btn btn-primary w-100">ثبت سفارش</button>
                </div>
            </div>
        </div>
    );
}