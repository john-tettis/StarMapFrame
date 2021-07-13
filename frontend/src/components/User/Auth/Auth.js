import React from 'react'

import Login from './Login';
import Register from './Register';

export default class Auth extends React.Component {
    constructor(props) {
        super(props);

        this.state = {checkForm: "login"};
        this.handleChangeForm = this.handleChangeForm.bind(this);
    }

    handleChangeForm(value) {
        this.setState({checkForm: value});
    }

    render() {
        if (this.state.checkForm === "login") {
            return <Login passToParent={this.handleChangeForm}/>
        }
        return <Register passToParent={this.handleChangeForm}/>
    }
}
