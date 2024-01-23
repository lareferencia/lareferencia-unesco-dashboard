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

      // Open the URL in a new tab
      window.open(url.href, "_blank");
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

  // Handling the button click event to open the default email client
  const handleEmail = () => {
    window.location.href = `mailto:${props.value}`;
  };

  // Render icons with some spacing
  return props.value !== "NO INFO"
    ? React.createElement(
        "div",
        null,
        isValidURL(props.value) &&
          React.createElement(
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
              style: { fontSize: "18px", color: "#007BFF", cursor: "pointer" },
              title: "Copiar URL al portapapeles",
            })
          ),
        !isValidURL(props.value) &&
          React.createElement("i", {
            className: "fas fa-copy",
            onClick: handleCopyToClipboard,
            style: { fontSize: "18px", color: "#007BFF", cursor: "pointer" },
            title: "Copiar URL al portapapeles",
          }),

        React.createElement("i", {
          className: "fas fa-envelope",
          onClick: handleEmail,
          style: {
            fontSize: "18px",
            color: "#007BFF",
            cursor: "pointer",
            marginLeft: "5px",
          },
          title: "Enviar correo electrónico",
        })
      )
    : React.createElement("i", {
        className: "fas fa-question-circle",
        style: {
          fontSize: "18px",
          color: "#999",
          cursor: "not-allowed",
          marginRight: "5px",
        },
        title: "No hay información de contacto",
      });
};

dagcomponentfuncs.WebButton = function (props) {
  return React.createElement("i", {
    className: "fas fa-external-link-square-alt",
    onClick: () => window.open(props.value, "_blank"),
    style: { fontSize: "18px", color: "#007BFF", cursor: "pointer" },
    title: "Ir al sitio web",
  });
};

dagcomponentfuncs.IniciativaComponent = function (props) {
  return React.createElement(
    "div",
    { style: { display: "flex", alignItems: "center" } },
    React.createElement("span", null, props.value),
    React.createElement("i", {
      className: "fas fa-arrow-right",
      style: { marginLeft: "5px", cursor: "pointer" },
    })
  );
};
