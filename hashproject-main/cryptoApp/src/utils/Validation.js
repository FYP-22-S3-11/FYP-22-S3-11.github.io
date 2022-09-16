import validator from "validator";

export const textFieldValidator = (min = 1, max = 20, val = "", req = true) => {
    let error = "";
    if (!val && req) {
        error = "Please fill this field!";
    } else if (val) {
        if (val.length < min) {
            error = `Min. length is ${min} characters!`;
        } else if (val.length > max) {
            error = `Max. length is ${max} characters!`;
        } else {
            if (!validator.isAlpha(val)) error = "Please enter only alphabets";
        }
    }
    return error;
};

export const textFieldNumberValidator = (min = 1, max = 10, val = "", req = true) => {
    let error = "";
    if (!val && req) {
        error = "Please fill this field!";
    } else if (val) {
        if (val.length < min) {
            error = `Min. length is ${min} characters!`;
        } else if (val.length > max) {
            error = `Max. length is ${max} characters!`;
        } else {
            if (!validator.isNumeric(val)) error = "Please enter only numbers";
        }
    }
    return error;
};