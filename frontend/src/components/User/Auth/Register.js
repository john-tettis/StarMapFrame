import React from 'react'

export default class Register extends React.Component {
    render() {
        return <div>
            <p>this is register form</p>
            <button type={"button"} onClick={()=> this.props.passToParent("login")}>Go to login</button>
        </div>
    }
}