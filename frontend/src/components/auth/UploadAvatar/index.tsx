import React, { useContext, useEffect, useRef, useState } from "react";
import { render } from "react-dom";
import { AuthContextProvider, AuthContext } from "../../../context/AuthContext";
import { getPermissions } from "../../../api/authApi";
import ProgressLinear from "../../status/ProgressLinear";
import getCookie from "../../../utils/getCookie";

const typesValid = ["image/png", "image/jpeg", "image/jpg"];

const UploadAvatar: React.FC = () => {
  const inputUploadRef = useRef<HTMLInputElement>(null);
  const [message, setMessage] = useState<string>("");
  const [isError, setIsError] = useState<boolean>(false);
  const [percentage, setPercentaje] = useState<number>(0);

  const { state, dispatch } = useContext(AuthContext);
  useEffect(() => {
    getPermissions(dispatch);
  }, [dispatch]);

  const handleOpenFileInput = () => {
    inputUploadRef.current?.click();
  };

  const onChangeInput = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files?.length) {
      for (let file of Array.from(files)) {
        if (!typesValid.includes(file.type)) {
          setMessage("El archivo no es una imagen.");
          setIsError(true);
          setPercentaje(0);
          return;
        }
        setIsError(false);

        const formData = new FormData();
        formData.append("avatar", file);

        const url = `/auth/avatar-upload/${state.user?.username}/`;

        const res = new XMLHttpRequest();
        res.open("PUT", url);
        res.setRequestHeader("X-CSRFToken", getCookie("csrftoken") ?? "");

        res.onreadystatechange = () => {
          if (res.readyState === XMLHttpRequest.DONE) {
            const status = res.status;
            if (status === 0 || (status >= 200 && status < 400)) {
              getPermissions(dispatch);
              setMessage("Avatar actualizado con éxito.");
            }
          }
        };

        res.upload.addEventListener("progress", ({ loaded, total }) => {
          setPercentaje(Math.floor(loaded / total) * 100);

          setTimeout(() => setPercentaje(0), 3000);
        });

        res.send(formData);
      }
    }
  };

  return (
    <>
      <div className="wrapper__avatar">
        <div className="avatar avatar-lg">
          <img
            alt={state.user?.full_name}
            src={state.user?.avatar ?? state.user?.avatar}
          />
        </div>
        <div className="form__avatar">
          <button
            className="btn btn-secondary btn-xsmall"
            onClick={handleOpenFileInput}
          >
            <i className="bx bx-upload bx-sm icon"></i>
            <span>Cambiar avatar</span>
          </button>
          <input
            type="file"
            onChange={onChangeInput}
            id="input-upload"
            ref={inputUploadRef}
          />
        </div>
      </div>
      {percentage > 4 && (
        <div className="mt-2">
          <ProgressLinear percentage={percentage} />
        </div>
      )}
      {message && (
        <div className={`alert alert-${isError ? "danger" : "success"} mt-2`}>
          {message}
        </div>
      )}
    </>
  );
};

export default UploadAvatar;

const containerUploadAvatar = document.getElementById("upload-avatar");
if (containerUploadAvatar) {
  render(
    <AuthContextProvider>
      <UploadAvatar />,
    </AuthContextProvider>,
    containerUploadAvatar
  );
}
