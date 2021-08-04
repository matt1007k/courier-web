import React, {
  ChangeEventHandler,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";
import { render } from "react-dom";
import { AuthContextProvider, AuthContext } from "../../../context/AuthContext";
import { getPermissions } from "../../../api/authApi";

const typesValid = ["image/png", "image/jpeg", "image/jpg"];
function getCookie(name: string) {
  // Split cookie string and get all individual name=value pairs in an array
  var cookieArr = document.cookie.split(";");

  // Loop through the array elements
  for (var i = 0; i < cookieArr.length; i++) {
    var cookiePair = cookieArr[i].split("=");

    /* Removing whitespace at the beginning of the cookie name
        and compare it with the given string */
    if (name == cookiePair[0].trim()) {
      // Decode the cookie value and return
      return decodeURIComponent(cookiePair[1]);
    }
  }

  // Return null if not found
  return null;
}

const UploadAvatar: React.FC = () => {
  const inputUploadRef = useRef<HTMLInputElement>(null);
  const [message, setMessage] = useState<string>("");
  const [isError, setIsError] = useState<boolean>(false);
  const [avatarUrl, setAvatarUrl] = useState<string | undefined>(
    "/static/img/avatar.png"
  );

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
          return;
        }
        setIsError(false);

        const formData = new FormData();
        formData.append("avatar", file);

        const headers = new Headers();
        headers.append("X-CSRFToken", getCookie("csrftoken") ?? "");

        fetch(`/auth/avatar-upload/${state.user?.username}/`, {
          method: "PUT",
          body: formData,
          headers,
        })
          .then((response) => response.json())
          .then((data) => {
            getPermissions(dispatch);
            setMessage("Avatar actualizado con éxito.");
          })
          .catch((error) => {
            console.error(error);
          });
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
