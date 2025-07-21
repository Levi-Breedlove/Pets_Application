// JavaScript functions for the registerWithValidation.html webpage

function formIsValid() {

    // Declare a validation flag and inititialize it to true.
    let valid = true;

    // Validate the telephone number using a regular expression.

    const US_PHONE_NUMBER = /^\d{3}-\d{3}-\d{4}$/;
    let phoneNumber = document.getElementById("phoneNumber").value;

    if (phoneNumber !== "") {
        if (!US_PHONE_NUMBER.test(phoneNumber)) {
            alert("Please enter a telephone number in the format xxx-xxx-xxxx");
            valid = false;
        }
    }

    // Return the value of the validation flag.
    return valid;
}

function processForm() {
    if (formIsValid()) {
        alert("Form submitted");
        return true;
    } else {
        return false;
    }
}