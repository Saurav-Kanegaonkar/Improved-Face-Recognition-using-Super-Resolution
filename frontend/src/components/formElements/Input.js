import React, { useReducer, useEffect } from "react";
import { validate } from "../../shared/utils/validators";

const inputReducer = (state, action) => {
  switch (action.type) {
    case "CHANGE":
      return {
        ...state,
        value: action.val,
        isValid: validate(action.val, action.validators),
      };
    case "TOUCH":
      return {
        ...state,
        isTouched: true,
      };
    default:
      return state;
  }
};

const Input = (props) => {
  const [inputState, dispatch] = useReducer(inputReducer, {
    value: "",
    isValid: false,
    isTouched: false,
  });

  useEffect(() => {
    props.onInput(props.id, inputState.value, inputState.isValid);
  }, [props.id, props.onInput, inputState.value, inputState.isValid]);

  const changeHandler = (event) => {
    dispatch({
      type: "CHANGE",
      val: event.target.value,
      validators: props.validators,
    });
  };
  const touchHandler = () => {
    dispatch({ type: "TOUCH" });
  };

  const element =
    props.element === "input" ? (
      <input
        className="form-control"
        id={props.id}
        type={props.type}
        onWheel={ event => event.currentTarget.blur() }
        placeholder={props.placeholder}
        onBlur={touchHandler}
        onChange={changeHandler}
        value={inputState.value}
      />
    ) : (
      
      <div>
        <div className="form-check form-check-inline">
          <input onChange = {changeHandler} className="form-check-input" type="radio" name="props.id" id="Admin" value="Admin"/>
          <label className="form-check-label" htmlFor="admin">Admin</label>
        </div>
        <div className="form-check form-check-inline">
            <input onChange = {changeHandler} className="form-check-input" type="radio" name="props.id" id="Teacher" value="Teacher"/>
            <label className="form-check-label" htmlFor="teacher">Teacher</label>
        </div>
        <div className="form-check form-check-inline">
            <input onChange = {changeHandler} className="form-check-input" type="radio" name="props.id" id="Student" value="Student"/>
            <label className="form-check-label" htmlFor="student">Student</label>
        </div>
      </div>
      // <select name="role" id="props.id" onChange = {changeHandler}>
      //   <option value="Admin">Admin</option>
      //   <option value="Teacher">Teacher</option>
      //   <option value="Student">Student</option>
      // </select>
      
    );
  return (
    <div>
      <label
        className={`form-label${
          !inputState.isValid && inputState.isTouched && "is-invalid"
        }`}
        htmlFor={props.id}
      >
        {props.label}
      </label>
      {element}
      {!inputState.isValid && inputState.isTouched && <p>{props.errorText}</p>}
    </div>
  );
};
export default Input;