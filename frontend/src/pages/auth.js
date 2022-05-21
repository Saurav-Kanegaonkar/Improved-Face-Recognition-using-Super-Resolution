import React, { useState, useContext } from "react";
import { Link } from "react-router-dom";
import { useForm } from "../hooks/form-hook";
import { AuthContext } from "../context/authContext";
import {
  VALIDATOR_EMAIL,
  VALIDATOR_REQUIRE,
  VALIDATOR_MINLENGTH,
} from "../shared/utils/validators";
import Input from "../components/formElements/Input";

const Auth = () => {
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
      const response = await fetch("http://localhost:5000/register", {
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
      if (!response.ok) {
        alert(responseData.message);
        throw new Error(responseData.message);
      }
      console.log(responseData);
      window.location.href = "/lectures";
    } catch (err) {
      console.log(err);
    }
  };

  // <form onSubmit={submitHandler}>
  //   <Input id="id_input" element="input" type="text" label="Id" errorText={"please enter a valid id"} validators={[VALIDATOR_REQUIRE()]} onInput={InputHandler} />
  //   <Input id="password_input" element="input" type="password" label="Password" errorText={"please enter a valid password longer than 6 characters"} validators={[VALIDATOR_MINLENGTH(6)]} onInput={InputHandler} />
  //   <div>
  //     <Input id="role_input" element="dropdown" type="text" label="Choose role" validators={[VALIDATOR_REQUIRE()]} onInput={InputHandler} />
  //   </div>
  //   <button className={`btn btn-primary ${ !formState.isValid ? "bg-black" : "grow " }`} type="submit" disabled={!formState.isValid}>
  //     SUBMIT
  //   </button>
  //   <Link style={{color: 'white'}} className="form-label" to="/login"> I have registered{" "}</Link>
  // </form>

  return (
    <div className="container card text-white bg-dark" style={{width: "32rem", marginTop: "7rem", textAlign: "left"}}>
        <div className="card-body">
            <h4 className="card-title" style={{textAlign: "center"}}>Register</h4>
            <form onSubmit={submitHandler}>
                <div className="mb-3">
                    <Input id="college_id" element="input" label="College ID" type="text" errorText={"Please enter a valid college ID"} validators={[VALIDATOR_MINLENGTH(6)]} onInput={InputHandler} />
                </div>
                <div className="mb-3">
                    <Input id="password" element="input" label="Password" type="password" errorText={"Please enter a valid password longer than 6 characters"} validators={[VALIDATOR_MINLENGTH(6)]} onInput={InputHandler} />
                </div>
                <div className="mb-3">
                    <Input id="role" element="radio" type="text" label="Choose role" onInput={InputHandler} validators={[VALIDATOR_REQUIRE()]} />
                </div>
                <div className="row">
                    <div className="col-4">
                        <button className={`btn btn-primary ${ !formState.isValid ? "bg-black" : "grow " }`} type="submit" disabled={!formState.isValid} >
                          SUBMIT
                        </button>
                    </div>
                    <div className="col-8 mt-1">
                        <Link style={{color: 'white'}} className="form-label" to="/login"> Already registered? Click here to login </Link>
                    </div>
                </div>
            </form>
        </div>
    </div>
  );
};
export default Auth;