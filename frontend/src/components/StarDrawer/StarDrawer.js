import React, {useState, useReducer} from 'react';

import Placeholder from "./Placeholder";
import StarGenerator from './StarGenerator';
import {v4 as uuidv4} from "uuid";


export default function StarDrawer() {
    const [filename, setFileUpdate] = useState({name: uuidv4().toString()+".svg", isReady: false, hash: Date.now()})
    return (
        <div className="container">
            <div className="row my-3">
                <div className="col-12">
                    <h1 className="text-center">تابلوی ستاره‌ای خود را بسازید!</h1>
                </div>
            </div>
            <div className="row">
                <div className="col-lg-6 col-md-6 col-sm-12">
                    <StarGenerator setFileUpdate={setFileUpdate} filename={filename}/>
                </div>
                <div className="col-lg-6 col-md-6 col-sm-12">
                    <Placeholder filename={filename}/>
                </div>
            </div>
        </div>
    );
}