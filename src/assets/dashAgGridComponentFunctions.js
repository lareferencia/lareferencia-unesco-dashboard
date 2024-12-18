var dagcomponentfuncs = (window.dashAgGridComponentFunctions =
  window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.ContactoButton = function (props) {
  // Function to check if a string is a valid URL
  const isValidURL = (url) => {
    try {
      new URL(url);
      return true;
    } catch (error) {
      return false;
    }
  };

  // Handling the button click event to navigate to the specified URL
  const handleNavigate = () => {
    try {
      // Attempt to create a URL object
      const url = new URL(props.value);

      // Open the URL in a new tab with rel="noopener noreferrer"
      const newWindow = window.open(url.href, "_blank");
      if (newWindow) {
        newWindow.opener = null;
        newWindow.rel = "noopener noreferrer";
      }
    } catch (error) {
      // Log the error and show an alert for an invalid URL
      console.error("Invalid URL:", props.value);
      alert("Invalid URL. Please provide a valid URL.");
    }
  };

  // Handling the button click event to copy the URL to the clipboard
  const handleCopyToClipboard = () => {
    try {
      // Attempt to copy the URL to the clipboard
      navigator.clipboard.writeText(props.value);
      alert("URL copied to clipboard!");
    } catch (error) {
      console.error("Unable to copy to clipboard:", error);
      alert("Failed to copy URL to clipboard.");
    }
  };

  // Handling the button click event to copy the URL to the clipboard
  const handleCopyToClipboardNoInfo = () => {
    alert("No URL available to copy to clipboard for this contact for now.");
  };

  // Handling the button click event to open the default email client
  const handleEmail = () => {
    window.location.href = `mailto:${props.value}`;
  };

  // Render icons with some spacing
  return props.value !== "NO INFO"
    ? React.createElement(
        "div",
        null,
        isValidURL(props.value)
          ? React.createElement(
              React.Fragment,
              null,
              React.createElement("i", {
                className: "fas fa-link",
                onClick: handleNavigate,
                style: {
                  fontSize: "18px",
                  color: "#007BFF",
                  cursor: "pointer",
                  marginRight: "5px",
                },
                title: "Ir a la página web de contacto",
              }),
              React.createElement("i", {
                className: "fas fa-copy",
                onClick: handleCopyToClipboard,
                style: {
                  fontSize: "18px",
                  color: "#007BFF",
                  cursor: "pointer",
                },
                title: "Copiar URL al portapapeles",
              })
            )
          : React.createElement(
              React.Fragment,
              null,
              React.createElement("i", {
                className: "fas fa-envelope",
                onClick: handleEmail,
                style: {
                  fontSize: "18px",
                  color: "#007BFF",
                  cursor: "pointer",
                  marginRight: "5px",
                },
                title: "Enviar correo electrónico",
              }),
              React.createElement("i", {
                className: "fas fa-copy",
                onClick: handleCopyToClipboard,
                style: {
                  fontSize: "18px",
                  color: "#007BFF",
                  cursor: "pointer",
                },
                title: "Copiar URL al portapapeles",
              })
            )
      )
    : React.createElement("i", {
        className: "fas fa-exclamation-triangle",
        onClick: handleCopyToClipboardNoInfo,
        style: {
          fontSize: "18px",
          color: "#007BFF",
          cursor: "pointer",
        },
        title: "No hay información de contacto",
      });
};

dagcomponentfuncs.WebButton = function (props) {
  // Handling the button click event to copy the URL to the clipboard
  const handleCopyToClipboard = () => {
    try {
      // Attempt to copy the URL to the clipboard
      navigator.clipboard.writeText(props.value);
      alert("URL copied to clipboard!");
    } catch (error) {
      console.error("Unable to copy to clipboard:", error);
      alert("Failed to copy URL to clipboard.");
    }
  };

  return React.createElement(
    "react-fragment",
    null,

    React.createElement("i", {
      className: "fas fa-external-link-square-alt",
      onClick: () => window.open(props.value, "_blank"),
      style: {
        fontSize: "18px",
        color: "#007BFF",
        cursor: "pointer",
        marginRight: "5px",
      },
      title: "Ir al sitio web",
    }),

    React.createElement("i", {
      className: "fas fa-copy",
      onClick: handleCopyToClipboard,
      style: {
        fontSize: "18px",
        color: "#007BFF",
        cursor: "pointer",
      },
      title: "Copiar URL al portapapeles",
    })
  );
};

dagcomponentfuncs.IniciativaComponent = function (props) {
  return React.createElement(
    "div",
    {
      style: { display: "flex", alignItems: "center", cursor: "pointer" },
      title: "Ver más detalles",
    },

    React.createElement("span", null, props.value)
  );
};

dagcomponentfuncs.DetallesComponent = function (props) {
  return React.createElement(
    "div", // Contenedor
    {
      style: {
        display: "flex",
        justifyContent: "center", // Centrar horizontalmente
        alignItems: "center", // Centrar verticalmente
        height: "100%", // Establecer la altura del contenedor
      },
    },
    React.createElement("i", {
      className: "fas fa-eye",
      style: {
        fontSize: "18px",
        color: "#007BFF",
        cursor: "pointer",
      },
      title: "Ver más detalles",
    })
  );
};
