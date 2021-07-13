import React from 'react';

export default class Login extends React.Component {
    render() {
        return <div>
            <p>this is login form</p>
            <button type={"button"} onClick={() => this.props.passToParent("register")}>Go to register</button>
        </div>
    }
}
