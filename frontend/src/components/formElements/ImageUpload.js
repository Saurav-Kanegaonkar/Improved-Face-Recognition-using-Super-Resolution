import React, { useRef, useState, useEffect } from "react";

const ImageUpload = (props) => {
  const [isValid, setIsValid] = useState(false);
  const [previewUrl, setPreviewUrl] = useState();
  const [file, setFile] = useState();

  const filePickerRef = useRef();

  useEffect(() => {
    if (!file) return;
    const filereader = new FileReader();
    filereader.onload = () => {
      setPreviewUrl(filereader.result);
    };
    filereader.readAsDataURL(file);
  }, [file]);

  const pickedHandler = (event) => {
    let pickedFile;
    let fileIsValid = isValid;
    if (event.target.files && event.target.files.length == 1) {
      pickedFile = event.target.files[0];
      setFile(pickedFile);
      setIsValid(true);
      fileIsValid = true;
    } else setIsValid(false);
    props.onInput(props.id, pickedFile, fileIsValid);
  };

  const pickImageHandler = () => {
    filePickerRef.current.click();
  };
  return (
    <div>
      <input
        id={props.id}
        style={{ display: "none" }}
        type="file"
        ref={filePickerRef}
        accept=".jpg,.png,.jpeg"
        onChange={pickedHandler}
      />
      <div>
        <div className="preview">
          {previewUrl && (
            <img
              src={previewUrl}
              style={{ height: 200, width: "auto" }}
              alt="preview"
            />
          )}
        </div>
        <button
          className={`b ph3 pv2 input-reset ba b--black   pointer f6 dib ma2
          `}
          type="button"
          onClick={pickImageHandler}
        >
          PICK IMAGE
        </button>
      </div>
    </div>
  );
};
export default ImageUpload;
