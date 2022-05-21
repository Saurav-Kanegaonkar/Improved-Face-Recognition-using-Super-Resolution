import React, { useState, useContext } from "react";
import { Link } from "react-router-dom";
import { useForm } from "../hooks/form-hook";
import {
  VALIDATOR_INT,
  VALIDATOR_REQUIRE,
  VALIDATOR_MINLENGTH,
} from "../shared/utils/validators";
import Input from "../components/formElements/Input";
import { AuthContext } from "../context/authContext";

const Login = () => {
  const auth = useContext(AuthContext);
  const [formState, InputHandler] = useForm({
    college_id: {
      value: "",
      isValid: false,
    },
    password: {
      value: "",
      isValid: false,
    },
    'role':{
      value: "",
      isValid : true
    }
  });

  const submitHandler = async (event) => {
    event.preventDefault();
    console.log(formState);
    try {
      const response = await fetch("http://localhost:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          college_id: formState.inputs.college_id.value,
          password: formState.inputs.password.value,
          role: formState.inputs.role.value
        }),
      });

      const responseData = await response.json();
      if (response.status === 401) {
        alert(responseData.message);
        throw new Error(responseData.message);
      }
      console.log(responseData);
      window.location.href = "/lectures";
    } catch (err) {
      console.log(err);
    }
  };

    // <div>
    //   <form onSubmit={submitHandler}>
    //     <Input id="college_id" element="input" type="text" label="Id" errorText={"Please enter a valid college id"} validators={[VALIDATOR_MINLENGTH(6)]} onInput={InputHandler} />
    //     <Input id="password" element="input" type="password" label="password" errorText={"Please enter a valid password longer than 6 characters"} validators={[VALIDATOR_MINLENGTH(6)]} onInput={InputHandler} />
    //     <Input id="role_input" element="dropdown" type="text" label="Choose role" onInput={InputHandler} validators={[VALIDATOR_REQUIRE()]} />
    //     <button className={`btn btn-primary ${ !formState.isValid ? "bg-black" : "grow " }`} type="submit" disabled={!formState.isValid} >
    //       SUBMIT
    //     </button>
    //     <Link className="form-label" to="/auth"> Not Registered?{" "} </Link>
    //   </form>
    // </div>


  return (
    <div className="container card text-white bg-dark" style={{width: "32rem", marginTop: "7rem", textAlign: "left"}}>
        <div className="card-body">
            <h4 className="card-title" style={{textAlign: "center"}}>Login</h4>
            <form onSubmit={submitHandler}>
                <div className="mb-3">
                    {/* <label for="college_id" className="form-label">College ID</label> */}
                    <Input id="college_id" element="input" label="College ID" type="text" errorText={"Please enter a valid college ID"} validators={[VALIDATOR_MINLENGTH(6)]} onInput={InputHandler} />
                    {/* <input type="number" value="" className="form-control" name="college_id" id="college_id" aria-describedby="college_id" required /> */}
                </div>
                <div className="mb-3">
                    {/* <label for="password" className="form-label">Password</label> */}
                    <Input id="password" element="input" label="Password" type="password" errorText={"Please enter a valid password longer than 6 characters"} validators={[VALIDATOR_MINLENGTH(6)]} onInput={InputHandler} />
                    {/* <input type="password" value="" name="password" className="form-control" id="password" required/> */}
                </div>
                <div className="mb-3">
                    <Input id="role" element="radio" type="text" label="Choose role" onInput={InputHandler} validators={[VALIDATOR_REQUIRE()]} />
                </div>
                <div className="row">
                    <div className="col-5">
                        <button className={`btn btn-primary ${ !formState.isValid ? "bg-black" : "grow " }`} type="submit" disabled={!formState.isValid} >
                          SUBMIT
                        </button>
                        {/* <button type="submit" className="btn btn-primary" value="Save">Submit</button> */}
                    </div>
                    <div className="col-7 mt-1 pl-4">
                        <Link style={{color: 'white'}} className="form-label" to="/auth"> Haven't registered? Click here. </Link>
                        {/* <a style={{color: 'white'}} href="auth">Already registered? Click here to login.</a> */}
                    </div>
                </div>
            </form>
        </div>
    </div>
  );
};
export default Login;